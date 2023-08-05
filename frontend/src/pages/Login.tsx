import axios from "axios";
import { FormikHelpers } from "formik";
import { useContext } from "react";
import { useLocation, useNavigate } from "react-router";
import { AuthContext } from "src/AuthContext";
import { ToastContext } from "src/ToastContext";
import { useMutation } from "src/query";
import { Form, Formik } from "formik";
import * as yup from "yup";

import EmailField from "src/components/EmailField";
import FormActions from "src/components/FormActions";
import PasswordField from "src/components/PasswordField";
import Title from "src/components/Title";

interface IForm {
    email: string;
    password: string;
}
const validationSchema = yup.object({
    email: yup.string().email("Email invalid").required("Email is required"),
    password: yup.string().required("Password is required"),
})

const useLogin = () => {
    const location = useLocation();
    const navigate = useNavigate();
    const { addToast } = useContext(ToastContext);
    const { setAuthenticated } = useContext(AuthContext);
    const { mutateAsync: login } = useMutation(
        async (data: IForm) => await axios.post("/session/", data),
    );
    return async (
        data: IForm,
        { setFieldError }: FormikHelpers<IForm>,
    ) => {
        try {
            await login(data);
            setAuthenticated(true);
            navigate((location.state as any)?.from ?? "/");
        } catch (error: any) {
            if (error.response?.status === 401) {
                setFieldError("email", "Invalid credentials");
                setFieldError("password", "Invalid credentials");
            } else {
                addToast("Try again", "error");
            }
        }
    };
}
const Login = () => {
    const onSubmit = useLogin();
    const location = useLocation();
    return (
        <>
            <Title title="Login" />
            <Formik<IForm>
                initialValues={{
                    email: (location.state as any)?.email ?? "",
                    password: "",
                }}
                onSubmit={onSubmit}
                validationSchema={validationSchema}
            >
                {({ dirty, isSubmitting, values }) => (
                    <Form>
                        <EmailField
                            fullWidth label="Email" name="email" required
                        />
                        <PasswordField
                            autoComplete="password"
                            fullWidth
                            label="Password"
                            name="password"
                            required
                        />
                        <FormActions
                            disabled={!dirty}
                            isSubmitting={isSubmitting}
                            label="Login"
                            links={[
                                { label: "Reset password", to: "/forgot-password/", state: { email: values.email } },
                                { label: "Register", to: "/register/", state: { email: values.email } },
                            ]}
                        />
                    </Form>
                )}
            </Formik>
        </>
    )
}

export default Login;