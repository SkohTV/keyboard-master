import bcrypt from 'bcrypt';
import mongoose from 'mongoose';
import Users from './models/users.js';

// Function to encrypt a password
export async function encryptPassword(password) {
  const saltRounds = 10;
  const salt = await bcrypt.genSalt(saltRounds);
  const hash = await bcrypt.hash(password, salt);
  return hash;
}

// Function to compare a password with its hash
export async function comparePassword(password, hash) {
  const result = await bcrypt.compare(password, hash);
  return result;
}

// Check if a hashed password is the same as the one in database
export async function verifPassword(name, hash){
  const dataDB = await Users.find({'name': name});
  return dataDB[0].hashedPwd === hash;
}