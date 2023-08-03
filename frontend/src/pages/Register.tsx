import axios from "axios";
import { Form, Formik, FormikHelpers } from "formik";
import { useContext } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import { ToastContext } from "src/ToastContext";
import EmailField from "src/components/EmailField";
import FormActions from "src/components/FormActions";
import LazyPasswordWithStrengthField from "src/components/LazyLoadPasswordStrength";
import Title from "src/components/Title";
import { useMutation } from "src/query";
import * as yup from "yup";




interface IForm {
    email: string;
    password: string;
}

const validationSchema = yup.object({
    email: yup.string().email().required(),
    password: yup.string().required(),
})


const useRegister = () => {
    const navigate = useNavigate();
    const { addToast } = useContext(ToastContext);
    const { mutateAsync: register } = useMutation(
        async (data: IForm) => await axios.post("/members/", data),
    );

    return async (
        data: IForm,
        { setFieldError }: FormikHelpers<IForm>
    ) => {
        try {
            await register(data);
            addToast("Successfully registered", "success");
            navigate("/login/", { state: { email: data.email } });
        }
        catch (error: any) {
            if (error.response?.status === 400 && error.response?.data.code === "WEAK PASSWORD") {
                setFieldError("password", "Password is too weak");
            }
            else {
                addToast("Something went wrong", "error");
            }
        }
    }

}


const Register = () => {
    const location = useLocation();
    const onSubmit = useRegister();
    return (
        <>
            <Title title="Register " />
            <Formik<IForm>
                initialValues={{
                    email: (location.state as any)?.email || "",
                    password: "",
                }}
                onSubmit={onSubmit}
                validationSchema={validationSchema}
            >
                {({ dirty, isSubmitting, values }) => (
                    <Form>
                        <EmailField
                            fullWidth label="Email"
                            name="email"
                            required
                        />
                        <LazyPasswordWithStrengthField
                            autoComplete="new-password"
                            fullWidth
                            label="Password"
                            name="Password"
                            required
                        />
                        <FormActions
                            disabled={!dirty}
                            isSubmitting={isSubmitting}
                            label="Register"
                            links={[
                                {
                                    label: "Login", to: "/login/", state: {
                                        email: values.email
                                    }
                                },
                                {
                                    label: "Reset Password", to: "/forgot-password/", state: { email: values.email }
                                },
                            ]}
                        />
                    </Form>
                )}
            </Formik>
        </>
    )
}

export default Register;