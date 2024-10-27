import { Button, useDisclosure, Modal, ModalOverlay, ModalContent, ModalBody, ModalHeader, ModalCloseButton, ModalFooter, FormControl, FormLabel, Input, Flex, Textarea, Radio, RadioGroup, Stack, useToast } from "@chakra-ui/react"
import { useState } from "react";
import { BiAddToQueue } from 'react-icons/bi';
import { useBookStore } from "../../store/useBookStore";
import { useAuthStore } from "../../store/useAuthStore";

const CreateBookModal = () => {
    const toast = useToast();
    const { isOpen, onOpen, onClose } = useDisclosure();
    const [isLoading, setIsLoading] = useState(false);

    const { addBook } = useBookStore();
    const { token } = useAuthStore();
    const [formData, setFormData] = useState({
        title: "",
        author: "",
        description: "",
        image_url: "",
        genre: "",
        total_pages: "",
        current_page: 0,
        completed: false
    });

    const handleSubmit = async (e) => {
        try {
            e.preventDefault();
            setIsLoading(true);
            await addBook(formData, token);
            console.log(formData);
            onClose();
            toast({
                title: "Book added successfully!",
                description: "Your book has been added to the library.",
                status: "success",
                duration: 5000,
                isClosable: true,
            })

        } catch (error) {
            console.error(error);
            toast({
                title: "Error!",
                description: error.response.data.message,
                status: "error",
                duration: 5000,
                isClosable: true,
            })
        }finally{
            setIsLoading(false);
            setFormData({
                title: "",
                author: "",
                description: "",
                image_url: "",
                genre: "",
                total_pages: "",
                current_page: 0,
                completed: false
            });
        }
    }

    return (
        <>
            <Button onClick={onOpen}>
                <BiAddToQueue size={20} />
            </Button>

            <Modal isOpen={isOpen} onClose={onClose}>
                <ModalOverlay />
                <form onSubmit={handleSubmit}>
                    <ModalContent>
                        <ModalHeader> Add New Book</ModalHeader>
                        <ModalCloseButton />
                        <ModalBody>
                            {/* Form for adding new book */}
                                <FormControl>
                                    <FormLabel>Book Title</FormLabel>
                                    <Input placeholder="The Innovator's Dillema"
                                    value={formData.title}
                                    onChange={e => setFormData({
                                        ...formData,title: e.target.value
                                    })}
                                    />
                                </FormControl>
                                <FormControl>
                                    <FormLabel>Author</FormLabel>
                                    <Input placeholder=" Clayton Christensen"
                                        value={formData.author}
                                        onChange={e => setFormData({
                                            ...formData, author: e.target.value
                                        })}
                                    />
                                </FormControl>
                            <FormControl>
                                <FormLabel>Genre</FormLabel>
                                <Input placeholder="Business Theory"
                                    value={formData.genre}
                                    onChange={e => setFormData({
                                        ...formData, genre: e.target.value
                                    })}
                                />
                            </FormControl>
                            <FormControl>
                                <FormLabel>Link To Image Cover</FormLabel>
                                <Input placeholder="https://m.media-amazon.com/images/I/51E7heV8GdL._SY445_SX342_.jpg"
                                    value={formData.image_url}
                                    onChange={e => setFormData({
                                        ...formData, image_url: e.target.value
                                    })}
                                />
                            </FormControl>
                            <FormControl>
                                <FormLabel>Total Pages</FormLabel>
                                <Input
                                    value={formData.total_pages}
                                    onChange={e => setFormData({
                                        ...formData, total_pages: e.target.value
                                    })}
                                />
                            </FormControl>
                            <FormControl mt={6}>
                                <FormLabel>Description</FormLabel>
                                <Textarea
                                    resize={"none"}
                                    overflowY="hidden"
                                    placeholder="The Innovator's Dilemma: When New Technologies Cause Great Firms to Fail, first published in 1997, is the best-known work of the Harvard professor and businessman Clayton Christensen."
                                value={formData.description}
                                    onChange={e => setFormData({
                                        ...formData, description: e.target.value
                                    })}
                                />
                            </FormControl>
                        </ModalBody>

                        <ModalFooter>
                            <Button onClick={onClose} mr={3}>
                                Cancel
                            </Button>
                            <Button variant="primary" type="submit"
                                isLoading={isLoading}
                            >Add</Button>
                        </ModalFooter>
                    </ModalContent>
                </form>
            </Modal>
        </>)
}

export default CreateBookModal