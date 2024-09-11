import React from 'react'
import { useAuthStore } from '../store/useAuthStore'
import Hero from '../components/Hero/Hero';
import Nav from '../components/Navbar/Nav';

const Home = () => {
    const {isLoggedIn} = useAuthStore();

  return (
    isLoggedIn? (
        <>
        <Nav/>
        <h1>Welcome Home!</h1>
        </>
    ) : <Hero/>
  )
}

export default Home