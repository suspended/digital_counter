import React from 'react';
import { Link } from 'react-router-dom';

import {
    Container,
    Navbar,
    Nav
} from 'react-bootstrap';

function Header() {

    return(
        <Navbar id="header" bg="dark" variant="dark" expand="lg" sticky="top">
            <Container className="px-4 py-0 mt-0 mb-0 ">
                <Link to="/"><Navbar.Brand>DigiCounter</Navbar.Brand></Link>
                <Navbar.Toggle aria-controls="navbarSupportedContent"/>

                <Navbar.Collapse id="navbarSupportedContent">
                    <Nav className="mr-auto">
                        <Nav.Link as={Link} to="/stats">Statistics</Nav.Link>
                    </Nav>
                </Navbar.Collapse>
            </Container>
        </Navbar>
    );
}

export default Header;
