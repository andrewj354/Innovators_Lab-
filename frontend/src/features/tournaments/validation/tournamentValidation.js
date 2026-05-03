/**
 * Валідація для форм турнірів.
 */
import { isRequired } from '../../../shared/utils/validators';

/** Валідація форми створення/редагування турніру */
export function validateTournamentForm(formData) {
  const errors = {};

  const titleErr = isRequired(formData.title, 'Tournament title');
  if (titleErr) errors.title = titleErr;

  const gameErr = isRequired(formData.game, 'Game');
  if (gameErr) errors.game = gameErr;

  if (formData.regStart && formData.regEnd) {
    const start = new Date(formData.regStart);
    const end = new Date(formData.regEnd);
    if (end <= start) {
      errors.regEnd = 'End date must be after start date';
    }
  }

  return errors;
}
