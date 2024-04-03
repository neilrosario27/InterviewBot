// Import the functions you need from the SDKs you need
import { initializeApp } from "firebase/app";
import { getAuth, GoogleAuthProvider } from "firebase/auth";
import { getFirestore } from "@firebase/firestore";


const firebaseConfig = {
  apiKey: "AIzaSyDb2-Kk70jUJhUMNUMLpFiSav1Dz5C9Tmk",
  authDomain: "bhashini-ce64a.firebaseapp.com",
  projectId: "bhashini-ce64a",
  storageBucket: "bhashini-ce64a.appspot.com",
  messagingSenderId: "260609355930",
  appId: "1:260609355930:web:f288e7ad03069a3171ef23"
  //, measurementId: "G-KWJSWQRNV0"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
export const db = getFirestore(app);
export const auth = getAuth(app);
export const provider = new GoogleAuthProvider();