document.addEventListener('DOMContentLoaded', function () {
  document.querySelectorAll('input[data-phone]').forEach(function (input) {
    input.addEventListener('input', function () {
      let digits = input.value.replace(/\D/g, '');

      // Заменяем ведущую 8 на 7
      if (digits.startsWith('8')) digits = '7' + digits.slice(1);
      // Если первая цифра не 7 — добавляем
      if (digits.length > 0 && digits[0] !== '7') digits = '7' + digits;

      // Максимум 11 цифр
      digits = digits.slice(0, 11);

      // Форматируем: +7 (XXX) XXX-XX-XX
      let out = '';
      if (digits.length >= 1)  out = '+7';
      if (digits.length > 1)   out += ' (' + digits.slice(1, Math.min(4, digits.length));
      if (digits.length >= 4)  out += ')';
      if (digits.length > 4)   out += ' '  + digits.slice(4, Math.min(7, digits.length));
      if (digits.length > 7)   out += '-'  + digits.slice(7, Math.min(9, digits.length));
      if (digits.length > 9)   out += '-'  + digits.slice(9, 11);

      input.value = out;
    });

    // Перед отправкой — оставляем только цифры для бэкенда
    var form = input.closest('form');
    if (form) {
      form.addEventListener('submit', function () {
        input.value = input.value.replace(/\D/g, '');
      });
    }
  });
});
