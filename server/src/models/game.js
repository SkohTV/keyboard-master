import mongoose from 'mongoose';


//! Replace with int
const scheme = new mongoose.Schema({
	gameID: {type: Number, required: true},
	sentence: {type: String},
	player1ms: {type: Number, required: true},
	player1: {type: String},
	player2ms: {type: Number, required: true},
	player2: {type: String}
});

const Game = mongoose.model('Game', scheme, 'Game');


export default Game;