import './App.css';
import Login from './pieces/pages/login.jsx'
import Update from './pieces/pages/update.jsx'
import Register from './pieces/pages/register.jsx'
import ProtectedRoute from './pieces/components/protectedRoute.jsx';
import CookieProtectedRoute from './pieces/components/cookieProtectedRoute.jsx';
import Home from './pieces/pages/home.jsx'
import { BrowserRouter, Routes, Route} from 'react-router-dom';


function App() {
  return (
    <div>
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Login />} />
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
        <Route element = {<ProtectedRoute />}>
            <Route path="/update" element={<Update />} />
            </Route>
          <Route element = {<CookieProtectedRoute />}>
            <Route path="/home" element={<Home />} />
          </Route>
      </Routes>
    </BrowserRouter>
    </div>
  );
}

export default App;
