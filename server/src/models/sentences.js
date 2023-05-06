import mongoose from 'mongoose';


const scheme = new mongoose.Schema({
	string: {type: String, required: true},
	difficulty: {type: String, required: true}
})

const Sentences = mongoose.model('Sentences', scheme, 'Sentences');


export default Sentences;