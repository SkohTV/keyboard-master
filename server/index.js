import bodyParser from 'body-parser';
import dotenv from 'dotenv';
import express from 'express';
import mongoose from 'mongoose';

import { comparePassword, encryptPassword } from './src/password.js';

import Matchmaking from './src/models/matchmaking.js';
import Sentences from './src/models/sentences.js';
import Users from './src/models/users.js';


dotenv.config();
const app = express();
const port = 3000;
const dbUrl = process.env.MONGO_USER;


app.use(bodyParser.urlencoded({ extended: false }));
app.use(bodyParser.json());



mongoose.connect(dbUrl, { useNewUrlParser: true, useUnifiedTopology: true })
	.then(() => console.log('Connected to MongoDB...'))
	.catch(err => console.error('Could not connect to MongoDB...', err));


app.post('/send', async (req, res) => {
	const [type, user, pack] = [req.body.type, JSON.parse(req.body.user), JSON.parse(req.body.pack)];
	let data = null;
	let returnValue, hashedPwd, dataDB, allow;

	try {
		switch (type){
			case 'CreateUser':
				hashedPwd = await encryptPassword(pack.rawPwd);
				dataDB = await Users.find({'name': pack.name});

				if (!dataDB.length){
					data = new Users({ 'name': pack.name, 'hashedPwd': hashedPwd });
					await data.save();
					returnValue = hashedPwd;
					console.log(`Added user ${pack.name} to MongoDB database`);
				} else {
					returnValue = 'Denied';
				}	break;

			case 'LoginUser':
				dataDB = await Users.find({'name': pack.name});
				allow = await comparePassword(pack.rawPwd, dataDB[0].hashedPwd);
				returnValue = allow ? dataDB[0].hashedPwd : 'Denied'
				break;

			case 'JoinMatchmaking':
			case 'LeaveMatchmaking':
				data = new Matchmaking({ 'username': user.name, 'gamemodes': pack.gamemodes });
				await data.save();
				returnValue = 'Data saved successfully';
				break;
		} res.status(201).send(returnValue);
	}

	catch (err) {
		console.error(err);
		res.status(500).send('Internal server error');
	}
});


app.listen(port, () => console.log(`Listening on port ${port}...`));