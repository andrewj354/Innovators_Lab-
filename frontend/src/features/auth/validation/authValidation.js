/**
 * Валідація для auth-форм (реєстрація, логін).
 * Використовує загальні утиліти з shared/utils/validators.
 */
import { isRequired, isValidEmail, mustMatch } from '../../../shared/utils/validators';

export function validateRegistrationField(field, value, form) {
  switch (field) {
    case 'username': {
      const req = isRequired(value, 'Username');
      if (req) return req;
      if (!/^[a-zA-Z0-9_]+$/.test(value)) {
        return 'Username can only contain Latin letters, numbers and underscores';
      }
      if (value.length < 3 || value.length > 25) {
        return 'Username must be between 3 and 25 characters';
      }
      return null;
    }

    case 'email': {
      const req = isRequired(value, 'Email');
      if (req) return req;
      const fmt = isValidEmail(value);
      if (fmt) return 'Invalid email, example: example@gmail.com';
      return null;
    }

    case 'password': {
      const req = isRequired(value, 'Password');
      if (req) return req;
      const hasNumber = /\d/.test(value);
      const hasUpper = /[A-Z]/.test(value);
      const hasLower = /[a-z]/.test(value);
      const hasSpecial = /[!@#$%^&*()_+\-=[\]{};':"\\|,.<>/?]/.test(value);
      const isLongEnough = value.length >= 8;
      if (!isLongEnough || !hasNumber || !hasUpper || !hasLower || !hasSpecial) {
        return 'Password must have at least 1 number, capital and small cases, special character and at least 8 characters';
      }
      return null;
    }

    case 'confirmPassword': {
      const req = isRequired(value, 'Password confirmation');
      if (req) return 'Please confirm your password';
      const match = mustMatch(form.password, value, 'Passwords does not match');
      if (match) return match;
      return null;
    }

    default:
      return null;
  }
}

export function validateRegistrationForm(form) {
  const errors = {};
  const fields = ['username', 'email', 'password', 'confirmPassword'];

  for (const field of fields) {
    const error = validateRegistrationField(field, form[field], form);
    if (error) errors[field] = error;
  }

  return errors;
}

export function validateLoginForm(form) {
  const errors = {};

  const emailErr = isRequired(form.email, 'Email');
  if (emailErr) errors.email = emailErr;

  const passErr = isRequired(form.password, 'Password');
  if (passErr) errors.password = passErr;

  return errors;
}

// ─── Step 2: Profile Info ──────────────────────────────────────────────────

export function validateProfileField(field, value) {
  switch (field) {
    case 'firstName': {
      const req = isRequired(value, 'Name');
      if (req) return req;
      if (!/^[a-zA-Z'-]+$/.test(value)) {
        return 'Name can only contain Latin letters, hyphen and apostrophe';
      }
      if (value.length < 3 || value.length > 25) {
        return 'Name must be between 3 and 25 characters';
      }
      return null;
    }

    case 'lastName': {
      const req = isRequired(value, 'Last name');
      if (req) return req;
      if (!/^[a-zA-Z'-]+$/.test(value)) {
        return 'Last name can only contain Latin letters, hyphen and apostrophe';
      }
      if (value.length < 3 || value.length > 25) {
        return 'Last name must be between 3 and 25 characters';
      }
      return null;
    }

    case 'dateOfBirth': {
      const req = isRequired(value, 'Date of birth');
      if (req) return req;
      const date = new Date(value);
      if (isNaN(date.getTime())) {
        return 'Invalid date';
      }

      const now = new Date();
      const age = now.getFullYear() - date.getFullYear();
      if (age < 13) return 'You must be at least 13 years old';
      if (age > 120) return 'Invalid date';
      return null;
    }

    default:
      return null;
  }
}

export function validateProfileForm(form) {
  const errors = {};
  const fields = ['firstName', 'lastName', 'dateOfBirth'];

  for (const field of fields) {
    const error = validateProfileField(field, form[field]);
    if (error) errors[field] = error;
  }

  return errors;
}

export function validateForgotPassword(email) {
  const req = isRequired(email, 'Email');
  if (req) return req;
  const fmt = isValidEmail(email);
  if (fmt) return 'Invalid email format';
  return null;
}

export function validateResetPassword(form) {
  const errors = {};

  const reqPass = isRequired(form.password, 'Password');
  if (reqPass) {
    errors.password = reqPass;
  } else {
    const hasNumber = /\d/.test(form.password);
    const hasUpper = /[A-Z]/.test(form.password);
    const hasLower = /[a-z]/.test(form.password);
    const hasSpecial = /[!@#$%^&*()_+\-=[\]{};':"\\|,.<>/?]/.test(form.password);
    const isLongEnough = form.password.length >= 8;
    if (!isLongEnough || !hasNumber || !hasUpper || !hasLower || !hasSpecial) {
      errors.password = 'Password must have at least 1 number, capital and small cases, special character and at least 8 characters';
    }
  }

  const reqConfirm = isRequired(form.confirmPassword, 'Password confirmation');
  if (reqConfirm) {
    errors.confirmPassword = 'Please confirm your password';
  } else {
    const match = mustMatch(form.password, form.confirmPassword, 'Passwords does not match');
    if (match) {
      errors.confirmPassword = match;
    }
  }

  return errors;
}
