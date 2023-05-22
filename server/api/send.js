import mongoose from 'mongoose';

import Game from '../src/models/game.js';
import Matchmaking from '../src/models/matchmaking.js';
import Sentences from '../src/models/sentences.js';
import Users from '../src/models/users.js';

import { comparePassword, encryptPassword, verifPassword } from '../src/password.js';
import { unpackGamemodes } from '../src/utils.js';


mongoose.connect(process.env.MONGO_USER, { useNewUrlParser: true, useUnifiedTopology: true })
	.then(() => console.log('Connected to MongoDB...'))
	.catch(err => console.error('Could not connect to MongoDB...', err));


export default async function send(req, res){
	const [type, user, pack] = [req.body.type, JSON.parse(req.body.user), JSON.parse(req.body.pack)];
	let returnValue, hashedPwd, dataDB, allow, gamemodes, gameDB, gameID;

	try {
		switch (type){
			case 'CreateUser':
				hashedPwd = await encryptPassword(pack.rawPwd);
				dataDB = await Users.find({'name': pack.name});
				if (dataDB.length){ returnValue = 'Denied' ; break ; }

				dataDB = new Users({ 'name': pack.name, 'hashedPwd': hashedPwd });
				await dataDB.save();
				console.log(`Added user ${pack.name} to MongoDB database`);
				returnValue = hashedPwd ; break ;

			case 'LoginUser':
				dataDB = await Users.find({'name': pack.name});
				if (!dataDB.length){ returnValue = 'Denied' ; break ; }
				allow = await comparePassword(pack.rawPwd, dataDB[0].hashedPwd);
				returnValue = allow ? dataDB[0].hashedPwd : 'Denied' ; break ;

			case 'JoinMatchmaking':
				if (!verifPassword(user.name, user.hashedPwd)){ returnValue = 'Denied' ; break ; }
				gamemodes = unpackGamemodes(pack.gamemodes);
				dataDB = await Matchmaking.findOne({'gamemodes': {$in: gamemodes}, 'player2': ''})
				if (dataDB){
					gameID = Math.floor(Math.random() * (999999999 - 100000000 + 1)) + 100000000;
					gameDB = new Game({'gameID': gameID, 'player1ms': 0, 'player2ms': 0, 'player2': user.name});
					dataDB.player2 = user.name;
					dataDB.gameID = gameID;
					await dataDB.save();
					await gameDB.save();

					const filteredGamemodes = dataDB.gamemodes.filter(x => gamemodes.includes(x))
					const sentenceDB = await Sentences.find({"type": {$in: filteredGamemodes[Math.floor(Math.random() * filteredGamemodes.length)]}});
					const manySentences = sentenceDB[Math.floor(Math.random() * sentenceDB.length)];
					const sentence = manySentences.sentences[Math.floor(Math.random() * manySentences.sentences.length)];
					gameDB.sentence = sentence;
					await gameDB.save()

					returnValue = dataDB.gameID;
					break;
				}
				dataDB = new Matchmaking({ 'gamemodes': gamemodes, 'player1': user.name, 'player2': ''});
				await dataDB.save();
				await new Promise(r => setTimeout(r, 5000));
				dataDB = await Matchmaking.findOne({'player1': user.name})
				if (!dataDB){ returnValue = 'Denied' ; break ; }
				if (dataDB.player2 != ''){
					returnValue = dataDB.gameID;
					dataDB = await Matchmaking.deleteMany({'player1': user.name});
					gameDB = await Game.findOne({'gameID': returnValue});
					gameDB.player1 = user.name;
					gameDB.save();
					break;
				}
				dataDB = await Matchmaking.deleteMany({'player1': user.name});
				returnValue = 'Denied' ; break ;

			case 'LeaveMatchmaking':
				if (!verifPassword(user.name, user.hashedPwd)){ returnValue = 'Denied' ; break ; }
				dataDB = await Matchmaking.deleteMany({'player1': user.name});
				returnValue = 'Allowed' ; break ;

			case 'SetMyScore':
				if (!verifPassword(user.name, user.hashedPwd)){ returnValue = 'Denied' ; break ; }
				dataDB = await Game.findOne({'gameID': pack.gameID})
				console.log(`${dataDB.player1 == user.name} - ${dataDB.player2 == user.name} - ${dataDB.player1ms < pack.score} - ${dataDB.player2ms} - ${dataDB.player2m} - ${pack.score}`)
				if (dataDB.player1 == user.name && dataDB.player1ms < pack.score){
					dataDB.player1ms = pack.score;
					await dataDB.save()
					returnValue = 'Allowed' ; break ;
				} else if (dataDB.player2 == user.name && dataDB.player2ms < pack.score){
					dataDB.player2ms = pack.score;
					await dataDB.save()
					returnValue = 'Allowed' ; break ;
				} returnValue = 'Denied'; break ;

			case 'RetrieveData':
				if (!verifPassword(user.name, user.hashedPwd)){ returnValue = 'Denied' ; break ; }
				dataDB = await Game.findOne({'gameID': pack.gameID})
				if (dataDB.player1 === user.name){
					returnValue = JSON.stringify({
						'player': dataDB.player2,
						'playerms': dataDB.player2ms,
						'sentence': dataDB.sentence
					})
					break ;
				}
				returnValue = JSON.stringify({
					'player': dataDB.player1,
					'playerms': dataDB.player1ms,
					'sentence': dataDB.sentence
				})
				break ;

			case 'QuerySentence':
				gamemodes = unpackGamemodes(pack.gamemodes);
				dataDB = await Sentences.find({"type": {$in: gamemodes}});
				const manySentences = dataDB[Math.floor(Math.random() * dataDB.length)];
				const sentence = manySentences.sentences[Math.floor(Math.random() * manySentences.sentences.length)]
				returnValue = sentence ; break ;
		} res.status(201).send(returnValue);
	}

	catch (err) {
		console.error(err);
		res.status(500).send('Internal server error');
	}
};