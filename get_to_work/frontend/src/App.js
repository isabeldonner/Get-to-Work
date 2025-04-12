import './App.css';
import Login from './pieces/pages/login.jsx'
import Home from './pieces/pages/home.jsx'
import Register from './pieces/pages/register.jsx'
import ProtectedRoute from './pieces/components/protectedRoute.jsx';
import { BrowserRouter, Routes, Route} from 'react-router-dom';


function App() {
  return (
    <div>
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Login />} />
        <Route path="/login" element={<Login />} />
        <Route element = {<ProtectedRoute />}>
           <Route path="/home" element={<Home />} />
        </Route>
        <Route path = "/register" element = {<Register />} />
      </Routes>
    </BrowserRouter>
    </div>
  );
}

export default App;
