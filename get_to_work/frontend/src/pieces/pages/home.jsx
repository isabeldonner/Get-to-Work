import React from 'react'



const Home = () => {
    const [userData, setUserData] = React.useState(null);
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
          setUserData(data);
        } catch (error) {
          console.error("Failed to fetch user info", error);
        }
      };
  
      if (username) fetchUserInfo();
    }, [username]);
  
    if (!userData) return <div>Loading...</div>;

  return (
    <div className="home-container">
    <h1>Welcome, {username}!</h1>
      <p>Your Completed Problems:</p>
      <ul>
        {userData.completedProblems?.map((problem, idx) => (
          <li key={idx}>{problem}</li>
        ))}
      </ul>
    </div>
  );
}

export default Home