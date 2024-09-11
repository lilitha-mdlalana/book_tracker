'use client'

import {
    Box,
    Flex,
    Avatar,
    Button,
    Menu,
    Link,
    MenuButton,
    MenuList,
    MenuItem,
    MenuDivider,
    useDisclosure,
    useColorModeValue,
    Stack,
    useColorMode,
    Center,
} from '@chakra-ui/react'
import { Link as ReactRouterLink } from 'react-router-dom'
import { MoonIcon, SunIcon } from '@chakra-ui/icons'
import { useAuthStore } from '../../store/useAuthStore'
import { useNavigate } from 'react-router-dom'


export default function Nav() {
    const { colorMode, toggleColorMode } = useColorMode()
    const { isOpen, onOpen, onClose } = useDisclosure()
    const { username, isLoggedIn, logout } = useAuthStore()
    const navigate = useNavigate();
    const handleLogout = () => {
        logout()
        navigate('/')
    }
    return (
        <>
            <Box bg={useColorModeValue('gray.100', 'gray.900')} px={4}>
                <Flex h={16} alignItems={'center'} justifyContent={'space-between'}>
                    <Box>Book Tracker</Box>

                    <Flex alignItems={'center'}>
                        <Stack direction={'row'} spacing={7}>
                            <Button onClick={toggleColorMode}>
                                {colorMode === 'light' ? <MoonIcon /> : <SunIcon />}
                            </Button>
                            {
                                isLoggedIn ? (

                                    <Menu>
                                        <MenuButton
                                            as={Button}
                                            rounded={'full'}
                                            variant={'link'}
                                            cursor={'pointer'}
                                            minW={0}>
                                            <Avatar
                                                size={'sm'}
                                                src={'https://avatar.iran.liara.run/public'}
                                            />
                                        </MenuButton>
                                        <MenuList alignItems={'center'}>
                                            <br />
                                            <Center>
                                                <p>{username}</p>
                                            </Center>
                                            <br />
                                            <MenuDivider />
                                            <MenuItem>
                                                <Link
                                                    to="/login"
                                                    onClick={handleLogout}
                                                    rounded={'full'}
                                                    px={6}
                                                    colorScheme={'white'}
                                                    bg={'red.400'}
                                                    _hover={{ bg: 'red.500' }}>
                                                    Logout
                                                </Link>


                                            </MenuItem>
                                        </MenuList>
                                    </Menu>
                                ) : (
                                    <>
                                        <Link
                                            as={ReactRouterLink}
                                            rounded={'full'}
                                            px={6}
                                            py={2}
                                            my={"auto"}
                                            colorScheme={'white'}
                                            bg={'orange.400'}
                                            _hover={{ bg: 'orange.500' }}
                                            to="/login" color={'white.400'}
                                            textAlign={"center"}
                                        >Login</Link>
                                    </>
                                )
                            }
                        </Stack>
                    </Flex>
                </Flex>
            </Box>
        </>
    )
}