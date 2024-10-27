import { create } from "zustand";
import { persist, createJSONStorage } from "zustand/middleware";
import axios from "axios";
import { BASEURL } from "../main";

export const useBookStore = create(
  persist(
    (set) => ({
      books: [],
      fetchBooks: async (accessToken) => {
        try {
          const response = await axios.get( BASEURL  + '/books', {
            headers: {
              Authorization: `Bearer ${accessToken}`,
            },
          });
          set({ books: response.data });
        } catch (error) {
          console.error('Failed to fetch books', error);
        }
      },
      addBook: async (book,accessToken) => {
        try {
          const response = await axios.post(`${BASEURL}/books`,book,{
            headers: {
              Authorization: `Bearer ${accessToken}`,
              'Content-Type': 'application/json',
            },
          })
          set((state) => ({ books: [...state.books, response.data] }));
        } catch (error) {
          throw new Error(error.message);
        }
      },
    }),
    {
      name: 'book-storage', // name of the item in storage
      storage: createJSONStorage(() => localStorage), // or sessionStorage
    },
  )
);