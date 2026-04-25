/**
 * Валідація для auth-форм (реєстрація, логін).
 * Використовує загальні утиліти з shared/utils/validators.
 */
import { isRequired, isValidEmail, minLength, mustMatch } from '../../../shared/utils/validators';

/** Валідація форми реєстрації */
export function validateRegistrationForm(form) {
  const errors = {};

  const firstNameErr = isRequired(form.firstName, 'First name');
  if (firstNameErr) errors.firstName = firstNameErr;

  const lastNameErr = isRequired(form.lastName, 'Last name');
  if (lastNameErr) errors.lastName = lastNameErr;

  const emailReqErr = isRequired(form.email, 'Email');
  if (emailReqErr) {
    errors.email = emailReqErr;
  } else {
    const emailFmtErr = isValidEmail(form.email);
    if (emailFmtErr) errors.email = emailFmtErr;
  }

  const passReqErr = isRequired(form.password, 'Password');
  if (passReqErr) {
    errors.password = passReqErr;
  } else {
    const passLenErr = minLength(form.password, 6, 'Password');
    if (passLenErr) errors.password = passLenErr;
  }

  const confirmReqErr = isRequired(form.confirmPassword, 'Password confirmation');
  if (confirmReqErr) {
    errors.confirmPassword = 'Please confirm your password';
  } else {
    const matchErr = mustMatch(form.password, form.confirmPassword, 'Passwords do not match');
    if (matchErr) errors.confirmPassword = matchErr;
  }

  return errors;
}

/** Валідація форми логіну */
export function validateLoginForm(form) {
  const errors = {};

  const emailErr = isRequired(form.email, 'Email');
  if (emailErr) errors.email = emailErr;

  const passErr = isRequired(form.password, 'Password');
  if (passErr) errors.password = passErr;

  return errors;
}
