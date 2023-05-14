import mongoose from 'mongoose';


//! Replace with int
const scheme = new mongoose.Schema({
	gameID: {type: Number, required: true},
	sentence: {type: String},
	player1ms: {type: Number, required: true},
	player2ms: {type: Number, required: true}
});

const Game = mongoose.model('Game', scheme, 'Game');


export default Game;