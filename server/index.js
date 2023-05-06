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
const port = process.env.PORT || 3000;
const dbUrl = process.env.MONGO_USER;


app.use(bodyParser.urlencoded({ extended: false }));
app.use(bodyParser.json());



mongoose.connect(dbUrl, { useNewUrlParser: true, useUnifiedTopology: true })
	.then(() => console.log('Connected to MongoDB...'))
	.catch(err => console.error('Could not connect to MongoDB...', err));


app.post('/send', async (req, res) => {
	console.log(req.body)
	const [type, user, pack] = [req.body.type, JSON.parse(req.body.user), JSON.parse(req.body.pack)];
	let data = null;

	try {
		switch (type){
			case 'CreateUser':
				
				const dataDB = await Users.find();
				const a = pack.rawPwd;
				const b = encryptPassword(a);
				console.log(a,b);
				console.log(comparePassword(a,b));
				break;

			case 'JoinMatchmaking':
			case 'LeaveMatchmaking':
				data = new Matchmaking({ 'username': user.name, 'gamemodes': pack.gamemodes });
				await data.save() ; break ;
		} res.status(201).send('Data saved successfully');
	} 

	catch (err) {
		console.error(err);
		res.status(500).send('Internal server error');
	}
});

app.get('/request', async (req, res) => {
	const [type, user, pack] = [req.body.type, JSON.parse(req.body.user), JSON.parse(req.body.pack)];
	let data = null;

	try {
		switch (type){
			case 'JSP': 
				const data = await Data.find();
				res.send(data);
		}
	}

	catch (err) {
			console.error(err);
			res.status(500).send('Internal server error');
	}
});


app.listen(port, () => console.log(`Listening on port ${port}...`));