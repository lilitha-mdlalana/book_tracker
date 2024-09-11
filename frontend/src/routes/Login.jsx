'use client'

import {
    Flex,
    Box,
    FormControl,
    FormLabel,
    Input,
    Checkbox,
    Stack,
    Button,
    Heading,
    Text,
    useColorModeValue,
    useToast,
} from '@chakra-ui/react'
import { useState } from 'react';
import Nav from '../components/Navbar/Nav'
import { useAuthStore } from '../store/useAuthStore';
import axios from 'axios';
import { BASEURL } from '../main';
import { useNavigate } from 'react-router-dom';

export default function Login() {
    const [username,setUsername] = useState();
    const [password, setPassword] = useState();
    const setUser = useAuthStore(state => state.setUser)
    const toast = useToast()
    const navigate = useNavigate();
    
    const handleLogin = async (event) => {
        event.preventDefault();
        try{
            const response = await axios.post(BASEURL + "login",{username,password});
            const {access_token} = response.data;

            setUser(username,access_token)
            localStorage.setItem('access_token', access_token);

            toast({
                title: "Login successful!",
                description: "Welcome back.",
                status: "success",
                duration: 5000,
                isClosable: true,
            })
            navigate('/')

        }catch(error){
            console.error(error);
            toast({
                title: "Error!",
                description: error.response.data.message,
                status: "error",
                duration: 5000,
                isClosable: true,
            })
        }
    }
    return (
        <>
            <Nav />
            <Flex
                minH={'100vh'}
                align={'center'}
                justify={'center'}
                bg={useColorModeValue('gray.50', 'gray.800')}>
                <Stack spacing={8} mx={'auto'} maxW={'lg'} py={12} px={6}>
                    <Stack align={'center'}>
                        <Heading fontSize={'4xl'}>Sign in to your account</Heading>
                        <Text fontSize={'lg'} color={'gray.600'}>
                            to enjoy all of our cool <Text as={"span"} color={'orange.400'}>features</Text> ✌️.
                        </Text>
                    </Stack>
                    <Box
                        rounded={'lg'}
                        bg={useColorModeValue('white', 'gray.700')}
                        boxShadow={'lg'}
                        p={8}>
                        <Stack spacing={4}>
                            <FormControl id="username">
                                <FormLabel>Username</FormLabel>
                                <Input type="text"
                                onChange={e => setUsername(e.target.value)}
                                />
                            </FormControl>
                            <FormControl id="password">
                                <FormLabel>Password</FormLabel>
                                <Input type="password"
                                onChange={e => setPassword(e.target.value)}
                                />
                            </FormControl>
                            <Stack spacing={10}>
                                <Button
                                    bg={'orange.400'}
                                    color={'white'}
                                    _hover={{
                                        bg: 'orange.500',
                                    }}
                                    onClick={handleLogin}
                                    >
                                    Sign in
                                </Button>
                            </Stack>
                        </Stack>
                    </Box>
                </Stack>
            </Flex>
        </>

    )
}