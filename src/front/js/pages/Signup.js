import React, { useState } from 'react';
import { useNavigate } from "react-router-dom";

export function Signup() {
    const navigate = useNavigate();
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [passwordConfirmation, setPasswordConfirmation] = useState('');
    const [errorMessage, setErrorMessage] = useState('');

    const handleSignup = () => {
        if (password !== passwordConfirmation) {
            setErrorMessage('Password and password confirmation do not match');
            return;
        }

        fetch('https://didactic-tribble-r47jpj7qggwxf54w7-3000.app.github.dev/api/signup', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ email, password })
        })
        .then((res) => res.json())
        .then((data) => {
            if (data.token) {
                sessionStorage.setItem('token', data.token);  // Usamos sessionStorage aquí
                setEmail('');
                setPassword('');
                setPasswordConfirmation('');
                navigate('/private');
            } else {
                setErrorMessage("Signup failed");
            }
        })
        .catch((err) => {
            setErrorMessage("Error: " + err.message || "Internal Server Error");
        });
    };

    return (
        <div style={{ display: 'flex', flexDirection: 'column', justifyContent: 'center', alignItems: 'center', height: '100vh' }}>
            <h2>Signup</h2>
            <form
                onSubmit={(e) => {
                    e.preventDefault();
                    handleSignup();
                }}
                style={{ display: 'flex', flexDirection: 'column', width: '30%' }}>
                <label>Email:</label>
                <input type="text" value={email} onChange={(e) => setEmail(e.target.value)} required />
                <label>Password:</label>
                <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} required />
                <label>Password Confirmation:</label>
                <input type="password" value={passwordConfirmation} onChange={(e) => setPasswordConfirmation(e.target.value)} required />
                <button type="submit" style={{ marginTop: '1rem' }}>Signup</button>
                {errorMessage && <p style={{ color: 'red', marginTop: '1rem' }}>{errorMessage}</p>}
            </form>
        </div>
    );
}
