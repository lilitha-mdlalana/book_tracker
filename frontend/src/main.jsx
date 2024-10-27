import { createRoot } from 'react-dom/client'
import App from './App.jsx'

import { createBrowserRouter, RouterProvider } from "react-router-dom";
import { ChakraProvider } from '@chakra-ui/react';

import Register from './routes/Register.jsx';
import Login from './routes/Login.jsx';
import Home from './routes/Home.jsx';

export const BASEURL= "http://localhost:5000/api";

const router = createBrowserRouter([
  {
    path: '/', element: <Home/>
  },
  { path: '/register', element: <Register /> },
  { path: '/login', element: <Login /> },
])
createRoot(document.getElementById('root')).render(
  <ChakraProvider>
    <RouterProvider router={router} />
  </ChakraProvider>,
)
