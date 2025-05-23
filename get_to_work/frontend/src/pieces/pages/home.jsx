import React from 'react'
import Collapsible from 'react-collapsible';
import './home.css'



const Home = () => {
    const [userData, setUserData] = React.useState(null);
    const [friendUsername, setFriendUsername] = React.useState(null);
    const username = localStorage.getItem("username");

  

  React.useEffect(() => {

    const fetchUserInfo = async () => {
      try {
        const response = await fetch(`http://localhost:8000/home`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ username }),
        });

        const data = await response.json();
        console.log("Fetched User Data:", data);
        setUserData(data);
      } catch (error) {
        console.error("Failed to fetch user info", error);
      }
    };
  
      if (username) fetchUserInfo();
    }, [username]);
  
    if (!userData) return <div>Loading...</div>;

    const friendRequest = async(event) => {
      event.preventDefault();
      const url = "http://localhost:8000/friendRequest/";
      
      const body = {username, friendUsername};
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

    } 
  } catch (error) {
    console.error("Error:", error);
    alert("Something went wrong. Try again.");
  }
}
    
    

  return (
    <div className = "body">
    <h1 className = "welcome">Welcome, {username}!</h1>
    <div className="completed-container">
      <div className = "titles">Your Completed Problems:</div>
      <ul style={{ listStyleType: "none"}}>
        {Object.entries(userData.completedProblems).map(([problemName, code], idx) => {
          const stats = userData.stats?.[problemName];
          console.log(stats);
          return(
          <li key={idx} className = "problems">
            <Collapsible trigger={problemName}>
              <pre style={{ whiteSpace: "pre-wrap", wordWrap: "break-word", fontSize: "11px" }}>
                {code}
              </pre>
              {stats ? (
          <div className="stats">
            <div><strong>Runtime:</strong> {stats.runtime}</div>
            <div><strong>Memory Usage:</strong> {stats.memory_usage}</div>
            <div><strong>Runtime Percentile:</strong> {stats.runtime_percentile}</div>
            <div><strong>Memory Percentile:</strong> {stats.memory_percentile}</div>
          </div>
        ) : (
          <div className = "stats">No stats available</div> 
        )}
            </Collapsible>
          </li>
          );
    })}
      </ul>
    </div>

    <div className="addFriend">
      <div className = "titles">Add a Friend:</div>
      <div className = "inputs">
      <input type="text" className = "input" placeholder="Enter username or email" value = {friendUsername} onChange = {(e)=>setFriendUsername(e.target.value)}/>
      </div>
      <form onSubmit = {friendRequest} style={{ display: "flex", justifyContent: "center" }}>
      <button className = "request">Request</button>
      </form>
    </div>

    <div className="requests-container">
      <div className = "titles">Friend Requests:</div>
      <ul style={{ listStyleType: "none"}}>
        {userData.friendRequests?.map((friend, idx) => (
          <li key={idx} className = "problems">{friend}
          <div>
          <button className = "accept">Accept</button>
          <button className = "decline">Decline</button>
          </div>
          </li>
        ))}
      </ul>
    </div>

    </div>
  );
}

export default Home