import {useEffect} from "react";
import {useBookStore} from "../../store/useBookStore";
import { useAuthStore } from "../../store/useAuthStore";

import { Container,Text,Grid,Flex } from "@chakra-ui/react"

import Book from "./Book";

const BookList = () => {
  const {books, fetchBooks} = useBookStore();
  const {token} = useAuthStore();

  useEffect(() => {
    if(token){
      fetchBooks(token);
    }
  }, [token,fetchBooks]);

  
    return (
      <Container maxWidth="container.xl">
        <Text 
        fontSize='2rem'
        fontWeight={'bold'}
        >Your books</Text>
        <Grid 
        gap={2}
        templateColumns={{
          base: '1fr',
          md: 'repeat(2,1fr)',
          lg: 'repeat(3,1fr)',
        }}
        >
          {books.length > 0 && books.map((book) => (
            <Book
              key={book.id}
              title={book.title}
              author={book.author}
              description={book.description}
              genre={book.genre}
              totalPages={book.total_pages}
              currentPage={book.current_page}
              imageUrl={book.image_url}
            />
          ))}
        </Grid>
        <div>
          {!books && <Flex justifyContent={"center"}>
            <Text> Poor you. No books found. 😔</Text>
          </Flex>}
        </div>
        </Container>
    );
}

export default BookList