import './App.css';
import Login from './pieces/pages/login.jsx'
import Update from './pieces/pages/update.jsx'
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
           <Route path="/update" element={<Update />} />
        </Route>
        <Route path = "/register" element = {<Register />} />
      </Routes>
    </BrowserRouter>
    </div>
  );
}

export default App;
