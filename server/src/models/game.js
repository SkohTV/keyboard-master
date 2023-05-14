import mongoose from 'mongoose';


//! Replace with int
const scheme = new mongoose.Schema({
	gameID: {type: Number, required: true},
	player1ms: {type: Number, required: true},
	player2ms: {type: Number, required: true}
});

const Game = mongoose.model('Matchmaking', scheme, 'Matchmaking');


export default Game;