// Global mocks for DOM APIs missing in jsdom
window.HTMLElement.prototype.scrollIntoView = jest.fn();
