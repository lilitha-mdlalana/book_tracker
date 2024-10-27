import React from 'react'
import { useAuthStore } from '../store/useAuthStore'
import Hero from '../components/Hero/Hero';
import Nav from '../components/Navbar/Nav';
import BookList from '../components/Book/BookList';

const Home = () => {
    const {isLoggedIn} = useAuthStore();

  return (
    isLoggedIn? (
        <>
        <Nav/>
        <BookList/>
        </>
    ) : <Hero/>
  )
}

export default Home