import axios from "axios";
import { Formik,Form } from "formik";
import { useContext } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import EmailField from "src/components/EmailField";
import FormActions from "src/components/FormActions";
import Title from "src/components/Title";
import { useMutation } from "src/query";
import { ToastContext } from "src/ToastContext";
import * as yup from "yup";

interface IForm {
    email: string;
}

const validationSchema = yup.object({
    email: yup.string().email("Email invalid").required("Required"),
})

const useForgottenPassword = () => {
    const navigate = useNavigate();
    const { addToast } = useContext(ToastContext);

    const { mutateAsync: forgotPassword } = useMutation(
        async (data: IForm) => await axios.post("/member/forgot_password", data),
    );
    return async (data: IForm) => {
        try {
            await forgotPassword(data);
            addToast("Resent link sent to email", "success");
            navigate("/login/");
        }
        catch (error: any) {
            addToast("Try again", "error");
        }
    }
}

const ForgotPasssword = () => {
    const onSubmit = useForgottenPassword();
    const location = useLocation();
    return (
        <>
            <Title title="Forgot Password" />
            <Formik<IForm>
                initialValues={{
                    email: (location.state as any)?.email ?? "",
                }}
                onSubmit={onSubmit}
                validationSchema={validationSchema}
            >
                {({ dirty, isSubmitting, values }) => (
                    <Form>
                        <EmailField
                            fullWidth
                            label="Email"
                            name="email"
                            required
                        />
                        <FormActions
                            disabled={!dirty}
                            isSubmitting={isSubmitting}
                            label="Send reset link"
                            links={
                                [
                                    { label: "Login", to: "/login/", state: { email: values.email } },
                                    { label: "Register", to: "/register/", state: { email: values.email } },
                                ]
                            }
                        />
                    </Form>
                )}
            </Formik>
        </>
    )
}
export default ForgotPasssword;