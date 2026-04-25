/**
 * Загальні утиліти валідації.
 * Використовуються в auth та tournament validation модулях.
 */

/** Перевірка що значення не пусте */
export function isRequired(value, fieldName) {
  if (!value || (typeof value === 'string' && !value.trim())) {
    return `${fieldName} is required`;
  }
  return null;
}

/** Перевірка email формату */
export function isValidEmail(email) {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  if (!emailRegex.test(email)) {
    return 'Enter a valid email address';
  }
  return null;
}

/** Перевірка мінімальної довжини */
export function minLength(value, min, fieldName) {
  if (value && value.length < min) {
    return `${fieldName} must be at least ${min} characters`;
  }
  return null;
}

/** Перевірка що два значення співпадають */
export function mustMatch(value1, value2, message = 'Values do not match') {
  if (value1 !== value2) {
    return message;
  }
  return null;
}
