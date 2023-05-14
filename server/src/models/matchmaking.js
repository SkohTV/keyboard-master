import mongoose from 'mongoose';


const scheme = new mongoose.Schema({
	gamemodes: {type: [String], required: true},
	gameID: {type: Number},
	player1: {type: String, required: true},
	player2: {type: String}
});

const Matchmaking = mongoose.model('Matchmaking', scheme, 'Matchmaking');


export default Matchmaking;