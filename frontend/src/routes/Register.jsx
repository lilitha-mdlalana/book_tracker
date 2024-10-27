'use client'

import {
    Flex,
    Box,
    FormControl,
    FormLabel,
    Input,
    InputGroup,
    HStack,
    InputRightElement,
    Stack,
    Button,
    Heading,
    Text,
    useColorModeValue,
    Link,
    useToast
} from '@chakra-ui/react'
import { useNavigate } from "react-router-dom"

import axios from "axios"
import { useState } from 'react'
import { ViewIcon, ViewOffIcon } from '@chakra-ui/icons'
import { Link as ReactRouterLink } from "react-router-dom"
import Nav from '../components/Navbar/Nav'
import { BASEURL } from '../main'

export default function Register() {
    const [showPassword, setShowPassword] = useState(false)
    const [username, setUsername] = useState("")
    const [password, setPassword] = useState("")
    const [confirmPassword, setConfirmPassword] = useState("")
    const toast = useToast()
    const navigate = useNavigate();


    const handleSubmit = async (event) => {
        event.preventDefault()
        console.log(username)
        console.log(password)
        if (password !== confirmPassword) {
            toast({
                title: "Passwords don't match!",
                description: "Please re-enter your password correctly.",
                status: "error",
                duration: 5000,
                isClosable: true,
            })
            return;
        }
        try {
            const response = await axios.post(BASEURL + "/register", {
                username,
                password
            });
            toast({
                title: "Registration successful!",
                description: "You can now log in with your credentials.",
                status: "success",
                duration: 5000,
                isClosable: true,
            })
            setUsername("")
            setPassword("")
            setConfirmPassword("")
            navigate("/login")
        } catch (e) {
            toast({
                title: "Registration failed!",
                description: "An error occurred while trying to register you. Please try again later.",
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
                        <Heading fontSize={'4xl'} textAlign={'center'}>
                            Sign up
                        </Heading>
                        <Text fontSize={'lg'} color={'gray.600'}>
                            to enjoy all of our cool features ✌️
                        </Text>
                    </Stack>
                    <Box
                        rounded={'lg'}
                        bg={useColorModeValue('white', 'gray.700')}
                        boxShadow={'lg'}
                        p={8}>
                        <Stack spacing={4}>
                            <Box>
                                <FormControl id="username" isRequired>
                                    <FormLabel>Username</FormLabel>
                                    <Input type="text" onChange={(e) => setUsername(e.target.value)} />
                                </FormControl>
                            </Box>
                            <FormControl id="password" isRequired>
                                <FormLabel>Password</FormLabel>
                                <InputGroup>
                                    <Input
                                        type={showPassword ? 'text' : 'password'}
                                        onChange={(e) => setPassword(e.target.value)} />
                                    <InputRightElement h={'full'}>
                                        <Button
                                            variant={'ghost'}
                                            onClick={() => setShowPassword((showPassword) => !showPassword)}>
                                            {showPassword ? <ViewIcon /> : <ViewOffIcon />}
                                        </Button>
                                    </InputRightElement>
                                </InputGroup>
                            </FormControl>
                            <FormControl id="confirmPassword" isRequired>
                                <FormLabel>Confirm Password</FormLabel>
                                <InputGroup>
                                    <Input type={showPassword ? 'text' : 'password'} onChange={(e) => setConfirmPassword(e.target.value)} />
                                    <InputRightElement h={'full'}>
                                        <Button
                                            variant={'ghost'}
                                            onClick={() => setShowPassword((showPassword) => !showPassword)}>
                                            {showPassword ? <ViewIcon /> : <ViewOffIcon />}
                                        </Button>
                                    </InputRightElement>
                                </InputGroup>
                            </FormControl>
                            <Stack spacing={10} pt={2}>
                                <Button
                                    loadingText="Submitting"
                                    size="lg"
                                    bg={'orange.400'}
                                    color={'white'}
                                    _hover={{
                                        bg: 'orange.500',
                                    }}
                                    type='Submit'
                                    onClick={handleSubmit}
                                >
                                    Sign up
                                </Button>
                            </Stack>
                            <Stack pt={6}>
                                <Text align={'center'}>
                                    Already a user? <Link as={ReactRouterLink} to="/login" color={'orange.400'}>Login</Link>
                                </Text>
                            </Stack>
                        </Stack>
                    </Box>
                </Stack>
            </Flex>
        </>

    )
}