import axios from "axios";
import { FormikHelpers } from "formik";
import { useContext } from "react";
import { useNavigate } from "react-router-dom";
import { ToastContext } from "src/ToastContext";
import { useMutation } from "src/query";
import Title from "src/components/Title";
import { Formik, Form } from "formik";
import * as yup from "yup";
import PasswordField from "src/components/PasswordField";
import LazyPasswordWithStrengthField from "src/components/LazyLoadPasswordStrength";
import FormActions from "src/components/FormActions";

interface iForms {
    currentPassword: string;
    newPassword: string;
}
const validationSchema = yup.object({
    currentPassword: yup.string().required("Required"),
    newPassword: yup.string().required("Required"),
})


const useChangePassword = () => {
    const { addToast } = useContext(ToastContext);
    const { mutateAsync: changePassword } = useMutation(
        async (data: iForms) => await axios.put("/members/password", data),
    )
    const navigate = useNavigate();

    return async (
        data: iForms,
        { setFieldError }: FormikHelpers<iForms>,
    ) => {
        try {
            await changePassword(data);
            addToast("Password Changed", "success");
            navigate("/");
        }
        catch (error: any) {
            if (axios.isAxiosError(error)) {
                if (error.response?.status === 400) {
                    setFieldError("newPassword", "Password too weak");
                }
                else if (error.response?.status === 401) {
                    setFieldError("currentPassword", "Incorrect Password");
                }
                else {
                    addToast("Something went wrong", "error");
                }
            }
        };
    }
}

const ChangePassword = () => {
    const onSubmit = useChangePassword();
    return (
        <>
            <Title title="Change Password" />
            <Formik<iForms>
                initialValues={{ currentPassword: "", newPassword: "" }}
                onSubmit={onSubmit}
                validationSchema={validationSchema}
            >
                {({ dirty, isSubmitting }) =>
                    <Form>
                        <PasswordField autoComplete="currentPassword" fullWidth label="Current password" name="currentPassword" required />
                        <LazyPasswordWithStrengthField autoComplete="new-password" fullWidth label="New password" name="newPassword" required />
                        <FormActions
                            disabled={!dirty}
                            isSubmitting={isSubmitting}
                            label="Change Password"
                            links={
                                [{
                                    label: "Back", to: "/"
                                }]
                            }
                        />
                    </Form>
                }

            </Formik>
        </>
    )
}
export default ChangePassword;