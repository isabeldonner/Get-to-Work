import React from 'react'
import './login.css'

import user_icon from '../assets/user.png'
import password_icon from '../assets/locked-computer.png'
import email_icon from '../assets/email.png'


const Login = () => {

    const [action, setAction] = React.useState("Sign Up");
    const [username, setUsername] = React.useState("");
    const [email, setEmail] = React.useState("");
    const [password, setPassword] = React.useState("");

    const handleSubmit = async(event) => {
        event.preventDefault();
        const url = action === "Sign Up" ? "http://localhost:8000/register/" : "http://localhost:8000/login/";
        
        const body = action === "Sign Up" ? {username: username, email, password} : {username, password};
        try{
          const response = await fetch(url, {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
            },
            body: JSON.stringify(body),
          });
        
          const data = await response.json();
      if (response.ok) {
        alert(data.message);
      } else {
        alert(data.detail);
      }
    } catch (error) {
      console.error("Error:", error);
      alert("Something went wrong. Try again.");
    }

      };
  return (
    <div className = 'container'>
      <div className = 'header'>
        <div className = 'text'>Get to Work!</div>
        <div className = 'loginsign'>{action}</div>
      </div>
      <div className = 'inputs'>
        <div className = 'input'>
            <img src = {user_icon} className = 'icon' alt = ''/>
            <input type = 'text' placeholder = {action === "Sign Up"?'Username': 'Username or email'} value = {username} onChange = {(e)=>setUsername(e.target.value)}/> 
        </div>
        <div className = {action === "Log In"?'hide': 'input'}>
            <img src = {email_icon} className = 'icon' alt = ''/>
            <input type = 'text' placeholder = 'Email' value = {email} onChange = {(e)=>setEmail(e.target.value)}/>
        </div>
        <div className = 'input'>
            <img src = {password_icon} className = 'icon' alt = ''/>
            <input type = 'text' placeholder = 'Password' value = {password} onChange = {(e)=>setPassword(e.target.value)}/> 
        </div>
      </div>
        <div className = 'submit-container'>
          <form onSubmit = {handleSubmit}>
            <button className = 'submit' type = 'submit'>{action}</button>
          </form>
            <div className = {action === "Log In"?'hide': 'acct'}>Already have an account? <span className = 'existing' onClick ={()=>setAction("Log In")}>Log in</span></div>
            <div className = {action === "Sign Up"?'hide': 'acct'}>New to Get to Work? <span className = 'existing' onClick ={()=>setAction("Sign Up")}>Create an account</span></div>
        </div>
    </div>
  ) 
}

export default Login