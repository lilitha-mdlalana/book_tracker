import { Box, Card, Image, Text, CardBody,Button,CardFooter,Progress } from "@chakra-ui/react"
import { BiTrash } from "react-icons/bi";

const Book = ({title,author, description, genre, totalPages,currentPage,completed,imageUrl}) => (
    <Card maxW="sm" overflow="hidden">
        <Image
            src={imageUrl}
            alt={title}
        />
        <CardBody gap={2}>
            <Progress 
                value={currentPage}
                max={totalPages}
                bgColor={'white'}
                colorScheme={'green'}
            />
            <Text>{currentPage}/{totalPages} pages read.</Text>
            <br />
            <Text
            fontSize={'1.5rem'}
            >{title}</Text>
            <Text
            fontSize={'0.9rem'}
            textAlign={'right'}
            fontStyle={'italic'}
            > - {author}</Text>
            
            <Text
                fontSize={'0.9rem'}
                isTruncated
            >{description}</Text>

            <Box display="flex" justifyContent="space-between" mt={2} mb={0}>
                <Text fontSize={'0.8rem'} fontWeight={'bold'}>Genre:</Text>
                <Text fontSize={'0.8rem'}
                >{genre}</Text>
            </Box>
        </CardBody>
        <CardFooter gap="2">
            <Button variant="solid">Update progress</Button>
            <Button variant="ghost">Add Quote</Button>
        </CardFooter>
    </Card>
    );

export default Book;