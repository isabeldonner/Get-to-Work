import React from 'react'
import {useNavigate} from 'react-router-dom'
import './login.jsx'
import './update.css'

const Update = () => {
    const [leetcodeSesh, setSession] = React.useState("");
    const [csrfToken, setToken] = React.useState("");
    const storedUsername = localStorage.getItem("username");
    const navigate = useNavigate();
        
    const handleSubmit = async(event) => {
      event.preventDefault();
      const url = "http://localhost:8000/update/";
      
      const body = {storedUsername, leetcodeSesh, csrfToken};
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
      navigate("/home");
    } else {
      alert(data.detail);
    }
  } catch (error) {
    console.error("Error:", error);
    alert("Something went wrong. Try again.");
  }

    };
    return (
        <div className = 'updatecontainer'>
              <div className = 'updateheader'>
                <div className = 'updateInfo'>Update Your Information</div>
                <div className = 'instructions'>To find your session information:</div>
                <div className = 'howto'>
                <ol>
                    <li>Login to Leetcode in another tab</li>
                    <li>Inspect Element on the Leetcode site</li>
                    <li>Go to the Applications tab</li>
                    <li>Scroll to the Storage section and then open the Cookies menu</li>
                    <li>Under Cookies, select the option for https://leetcode.com</li>
                    <li>Find the values for the cookies called LEETCODE_SESSION and csrftoken</li>
                </ol>
                </div>
              </div>
              <div className = 'inputs'>
                <div className = 'input'>
                    <input type = 'text' placeholder = 'Leetcode Session' value = {leetcodeSesh} onChange = {(e)=>setSession(e.target.value)}/> 
                </div>
                <div className = 'input'>
                    <input type = 'text' placeholder = 'CSRF Token' value = {csrfToken} onChange = {(e)=>setToken(e.target.value)}/> 
                </div>
              </div>
                <div className = 'submit-container'>
                  <form onSubmit = {handleSubmit}>
                    <button className = 'submit' type = 'submit'>Update</button>
                  </form>
                </div>
            </div>
    )
}

export default Update