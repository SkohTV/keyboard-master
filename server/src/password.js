import bcrypt from 'bcrypt';


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