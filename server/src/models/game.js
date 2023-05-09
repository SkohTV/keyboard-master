import mongoose from 'mongoose';


//! Replace with int
const scheme = new mongoose.Schema({
	gameID: {type: Int16Array, required: true},
	player1ms: {type: Float64Array, required: true},
	player2ms: {type: Float64Array, required: true}
});

const Matchmaking = mongoose.model('Matchmaking', scheme, 'Matchmaking');


export default Matchmaking;