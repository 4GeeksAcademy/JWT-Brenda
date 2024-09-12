import React, { useContext, useEffect} from "react";
import { useNavigate } from "react-router-dom";
import { Context } from "../store/appContext";
import "../../styles/home.css";

export const Home = () => {
	const navigate = useNavigate();
	const { store, actions } = useContext(Context);

	useEffect(() => {

		const authToken = localStorage.getItem('auth_token');

		if (!authToken){
			navigate('/signup');
		} 
	}, []);

	return (
		<div className="text-center mt-5">
			<h1>Hello Rigo!!</h1>
		
			<div className="alert alert-info">
				{store.message || "Loading message from the backend (make sure your python backend is running)..."}
			</div>
			<p>
				This boilerplate comes with lots of documentation:{" "}
				<a href="https://start.4geeksacademy.com/starters/react-flask">
					Read documentation
				</a>
			</p>
		</div>
	);
};
