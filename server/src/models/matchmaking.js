import mongoose from 'mongoose';


const scheme = new mongoose.Schema({
	username: {type: String, required: true},
	gamemodes: {type: String, required: true}
});

const Matchmaking = mongoose.model('Matchmaking', scheme, 'Matchmaking');


export default Matchmaking;