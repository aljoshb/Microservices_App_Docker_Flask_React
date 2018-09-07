import React from 'react';

/* This Form component handles both registration and Login
 * with the inline if statment.
 */
const Form = (props) => {
    return (
        <div>
            <h1 className="title is-1">{props.formType}</h1>
            <hr/><br/>
            <form onSubmit={(event) => props.handleUserFormSubmit(event)}>
                {props.formType === 'Register' && // inline if statement
                    <div className="field"> 
                        <input
                            name="username"
                            className="input is-medium"
                            type="text"
                            placeholder="Enter a username" required
                            value={props.formData.username}
                            onChange={props.handleFormChange}
                        />
                    </div> // This only shows if this is a user registration
                }
                <div className="field">
                    <input
                        name="email"
                        className="input is-medium"
                        type="email"
                        placeholder="Enter an email address" required
                        value={props.formData.email}
                        onChange={props.handleFormChange}
                    />
                </div>
                <div className="field">
                    <input
                        name="password"
                        className="input is-medium"
                        type="password"
                        placeholder="Enter a password" required
                        value={props.formData.email}
                        onChange={props.handleFormChange}
                    />
                </div>
                <input
                    type="submit"
                    className="button is-primary is-medium is-fullwidth"
                    value="Submit"
                />
            </form>
        </div>
    )
};

export default Form;