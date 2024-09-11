import { create } from "zustand";

export const useAuthStore = create((set) => ({
  username: localStorage.getItem("username") || null,
  token: localStorage.getItem("access_token") || null,
  isLoggedIn: !!localStorage.getItem("access_token"),

  setUser: (username, token) =>{
    localStorage.setItem("username", username);
    set({
      username: username,
      accessToken: token,
      isLoggedIn: true,
    })},

  logout: () => {
    localStorage.removeItem("access_token");
    set({ token: null, isLoggedIn: false });
  },
}));
