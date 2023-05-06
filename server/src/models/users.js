import mongoose from 'mongoose';


const scheme = new mongoose.Schema({
	name: {type: String, required: true},
	hashedPwd: {type: String, required: true}
})

const Users = mongoose.model('Users', scheme, 'Users');


export default Users;