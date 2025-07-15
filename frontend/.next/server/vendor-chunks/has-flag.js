"use strict";
/*
 * ATTENTION: An "eval-source-map" devtool has been used.
 * This devtool is neither made for production nor for readable output files.
 * It uses "eval()" calls to create a separate source file with attached SourceMaps in the browser devtools.
 * If you are trying to read the output file, select a different devtool (https://webpack.js.org/configuration/devtool/)
 * or disable the default devtool with "devtool: false".
 * If you are looking for production-ready output files, see mode: "production" (https://webpack.js.org/configuration/mode/).
 */
exports.id = "vendor-chunks/has-flag";
exports.ids = ["vendor-chunks/has-flag"];
exports.modules = {

/***/ "(ssr)/./node_modules/has-flag/index.js":
/*!****************************************!*\
  !*** ./node_modules/has-flag/index.js ***!
  \****************************************/
/***/ ((module) => {

eval("\n\nmodule.exports = function (flag) {\n  var argv = arguments.length > 1 && arguments[1] !== undefined ? arguments[1] : process.argv;\n  var prefix = flag.startsWith('-') ? '' : flag.length === 1 ? '-' : '--';\n  var position = argv.indexOf(prefix + flag);\n  var terminatorPosition = argv.indexOf('--');\n  return position !== -1 && (terminatorPosition === -1 || position < terminatorPosition);\n};//# sourceURL=[module]\n//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoiKHNzcikvLi9ub2RlX21vZHVsZXMvaGFzLWZsYWcvaW5kZXguanMiLCJtYXBwaW5ncyI6IkFBQWE7O0FBRWJBLE1BQU0sQ0FBQ0MsT0FBTyxHQUFHLFVBQUNDLElBQUksRUFBMEI7RUFBQSxJQUF4QkMsSUFBSSxHQUFBQyxTQUFBLENBQUFDLE1BQUEsUUFBQUQsU0FBQSxRQUFBRSxTQUFBLEdBQUFGLFNBQUEsTUFBR0csT0FBTyxDQUFDSixJQUFJO0VBQzFDLElBQU1LLE1BQU0sR0FBR04sSUFBSSxDQUFDTyxVQUFVLENBQUMsR0FBRyxDQUFDLEdBQUcsRUFBRSxHQUFJUCxJQUFJLENBQUNHLE1BQU0sS0FBSyxDQUFDLEdBQUcsR0FBRyxHQUFHLElBQUs7RUFDM0UsSUFBTUssUUFBUSxHQUFHUCxJQUFJLENBQUNRLE9BQU8sQ0FBQ0gsTUFBTSxHQUFHTixJQUFJLENBQUM7RUFDNUMsSUFBTVUsa0JBQWtCLEdBQUdULElBQUksQ0FBQ1EsT0FBTyxDQUFDLElBQUksQ0FBQztFQUM3QyxPQUFPRCxRQUFRLEtBQUssQ0FBQyxDQUFDLEtBQUtFLGtCQUFrQixLQUFLLENBQUMsQ0FBQyxJQUFJRixRQUFRLEdBQUdFLGtCQUFrQixDQUFDO0FBQ3ZGLENBQUMiLCJzb3VyY2VzIjpbIndlYnBhY2s6Ly9jb2RleC1ib29zdGVyLWZyb250ZW5kLy4vbm9kZV9tb2R1bGVzL2hhcy1mbGFnL2luZGV4LmpzP2YzZjYiXSwic291cmNlc0NvbnRlbnQiOlsiJ3VzZSBzdHJpY3QnO1xuXG5tb2R1bGUuZXhwb3J0cyA9IChmbGFnLCBhcmd2ID0gcHJvY2Vzcy5hcmd2KSA9PiB7XG5cdGNvbnN0IHByZWZpeCA9IGZsYWcuc3RhcnRzV2l0aCgnLScpID8gJycgOiAoZmxhZy5sZW5ndGggPT09IDEgPyAnLScgOiAnLS0nKTtcblx0Y29uc3QgcG9zaXRpb24gPSBhcmd2LmluZGV4T2YocHJlZml4ICsgZmxhZyk7XG5cdGNvbnN0IHRlcm1pbmF0b3JQb3NpdGlvbiA9IGFyZ3YuaW5kZXhPZignLS0nKTtcblx0cmV0dXJuIHBvc2l0aW9uICE9PSAtMSAmJiAodGVybWluYXRvclBvc2l0aW9uID09PSAtMSB8fCBwb3NpdGlvbiA8IHRlcm1pbmF0b3JQb3NpdGlvbik7XG59O1xuIl0sIm5hbWVzIjpbIm1vZHVsZSIsImV4cG9ydHMiLCJmbGFnIiwiYXJndiIsImFyZ3VtZW50cyIsImxlbmd0aCIsInVuZGVmaW5lZCIsInByb2Nlc3MiLCJwcmVmaXgiLCJzdGFydHNXaXRoIiwicG9zaXRpb24iLCJpbmRleE9mIiwidGVybWluYXRvclBvc2l0aW9uIl0sInNvdXJjZVJvb3QiOiIifQ==\n//# sourceURL=webpack-internal:///(ssr)/./node_modules/has-flag/index.js\n");

/***/ })

};
;