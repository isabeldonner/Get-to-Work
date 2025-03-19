import React from 'react'
import './login.css'

import user_icon from '../assets/user.png'
import password_icon from '../assets/locked-computer.png'
import email_icon from '../assets/email.png'


const Login = () => {

    const [action, setAction] = React.useState("Sign Up");

  return (
    <div className = 'container'>
      <div className = 'header'>
        <div className = 'text'>Get to Work!</div>
        <div className = 'loginsign'>{action}</div>
      </div>
      <div className = 'inputs'>
        <div className = 'input'>
            <img src = {user_icon} className = 'icon' alt = ''/>
            <input type = 'text' placeholder = {action === "Sign Up"?'Username': 'Username or email'}/> 
        </div>
        <div className = {action === "Log In"?'hide': 'input'}>
            <img src = {email_icon} className = 'icon' alt = ''/>
            <input type = 'text' placeholder = 'Email'/>
        </div>
        <div className = 'input'>
            <img src = {password_icon} className = 'icon' alt = ''/>
            <input type = 'text' placeholder = 'Password'/> 
        </div>
      </div>
        <div className = 'submit-container'>
            <button className = 'submit'>{action}</button>
            <div className = {action === "Log In"?'hide': 'acct'}>Already have an account? <span className = 'existing' onClick ={()=>setAction("Log In")}>Log in</span></div>
            <div className = {action === "Sign Up"?'hide': 'acct'}>New to Get to Work? <span className = 'existing' onClick ={()=>setAction("Sign Up")}>Create an account</span></div>
        </div>
    </div>
  ) 
}

export default Login