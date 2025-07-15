"use strict";
/*
 * ATTENTION: An "eval-source-map" devtool has been used.
 * This devtool is neither made for production nor for readable output files.
 * It uses "eval()" calls to create a separate source file with attached SourceMaps in the browser devtools.
 * If you are trying to read the output file, select a different devtool (https://webpack.js.org/configuration/devtool/)
 * or disable the default devtool with "devtool: false".
 * If you are looking for production-ready output files, see mode: "production" (https://webpack.js.org/configuration/mode/).
 */
exports.id = "vendor-chunks/snakecase-keys";
exports.ids = ["vendor-chunks/snakecase-keys"];
exports.modules = {

/***/ "(rsc)/./node_modules/snakecase-keys/index.js":
/*!**********************************************!*\
  !*** ./node_modules/snakecase-keys/index.js ***!
  \**********************************************/
/***/ ((module, __unused_webpack_exports, __webpack_require__) => {

eval("\n\nvar map = __webpack_require__(/*! map-obj */ \"(rsc)/./node_modules/map-obj/index.js\");\nvar _require = __webpack_require__(/*! snake-case */ \"(rsc)/./node_modules/snake-case/dist.es2015/index.js\"),\n  snakeCase = _require.snakeCase;\nmodule.exports = function (obj, options) {\n  options = Object.assign({\n    deep: true,\n    exclude: [],\n    parsingOptions: {}\n  }, options);\n  return map(obj, function (key, val) {\n    return [matches(options.exclude, key) ? key : snakeCase(key, options.parsingOptions), val];\n  }, options);\n};\nfunction matches(patterns, value) {\n  return patterns.some(function (pattern) {\n    return typeof pattern === 'string' ? pattern === value : pattern.test(value);\n  });\n}//# sourceURL=[module]\n//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoiKHJzYykvLi9ub2RlX21vZHVsZXMvc25ha2VjYXNlLWtleXMvaW5kZXguanMiLCJtYXBwaW5ncyI6IkFBQVk7O0FBRVosSUFBTUEsR0FBRyxHQUFHQyxtQkFBTyxDQUFDLHNEQUFTLENBQUM7QUFDOUIsSUFBQUMsUUFBQSxHQUFzQkQsbUJBQU8sQ0FBQyx3RUFBWSxDQUFDO0VBQW5DRSxTQUFTLEdBQUFELFFBQUEsQ0FBVEMsU0FBUztBQUVqQkMsTUFBTSxDQUFDQyxPQUFPLEdBQUcsVUFBVUMsR0FBRyxFQUFFQyxPQUFPLEVBQUU7RUFDdkNBLE9BQU8sR0FBR0MsTUFBTSxDQUFDQyxNQUFNLENBQUM7SUFBRUMsSUFBSSxFQUFFLElBQUk7SUFBRUMsT0FBTyxFQUFFLEVBQUU7SUFBRUMsY0FBYyxFQUFFLENBQUM7RUFBRSxDQUFDLEVBQUVMLE9BQU8sQ0FBQztFQUVqRixPQUFPUCxHQUFHLENBQUNNLEdBQUcsRUFBRSxVQUFVTyxHQUFHLEVBQUVDLEdBQUcsRUFBRTtJQUNsQyxPQUFPLENBQ0xDLE9BQU8sQ0FBQ1IsT0FBTyxDQUFDSSxPQUFPLEVBQUVFLEdBQUcsQ0FBQyxHQUFHQSxHQUFHLEdBQUdWLFNBQVMsQ0FBQ1UsR0FBRyxFQUFFTixPQUFPLENBQUNLLGNBQWMsQ0FBQyxFQUM1RUUsR0FBRyxDQUNKO0VBQ0gsQ0FBQyxFQUFFUCxPQUFPLENBQUM7QUFDYixDQUFDO0FBRUQsU0FBU1EsT0FBT0EsQ0FBRUMsUUFBUSxFQUFFQyxLQUFLLEVBQUU7RUFDakMsT0FBT0QsUUFBUSxDQUFDRSxJQUFJLENBQUMsVUFBVUMsT0FBTyxFQUFFO0lBQ3RDLE9BQU8sT0FBT0EsT0FBTyxLQUFLLFFBQVEsR0FDOUJBLE9BQU8sS0FBS0YsS0FBSyxHQUNqQkUsT0FBTyxDQUFDQyxJQUFJLENBQUNILEtBQUssQ0FBQztFQUN6QixDQUFDLENBQUM7QUFDSiIsInNvdXJjZXMiOlsid2VicGFjazovL2NvZGV4LWJvb3N0ZXItZnJvbnRlbmQvLi9ub2RlX21vZHVsZXMvc25ha2VjYXNlLWtleXMvaW5kZXguanM/MGVmMSJdLCJzb3VyY2VzQ29udGVudCI6WyIndXNlIHN0cmljdCdcblxuY29uc3QgbWFwID0gcmVxdWlyZSgnbWFwLW9iaicpXG5jb25zdCB7IHNuYWtlQ2FzZSB9ID0gcmVxdWlyZSgnc25ha2UtY2FzZScpXG5cbm1vZHVsZS5leHBvcnRzID0gZnVuY3Rpb24gKG9iaiwgb3B0aW9ucykge1xuICBvcHRpb25zID0gT2JqZWN0LmFzc2lnbih7IGRlZXA6IHRydWUsIGV4Y2x1ZGU6IFtdLCBwYXJzaW5nT3B0aW9uczoge30gfSwgb3B0aW9ucylcblxuICByZXR1cm4gbWFwKG9iaiwgZnVuY3Rpb24gKGtleSwgdmFsKSB7XG4gICAgcmV0dXJuIFtcbiAgICAgIG1hdGNoZXMob3B0aW9ucy5leGNsdWRlLCBrZXkpID8ga2V5IDogc25ha2VDYXNlKGtleSwgb3B0aW9ucy5wYXJzaW5nT3B0aW9ucyksXG4gICAgICB2YWxcbiAgICBdXG4gIH0sIG9wdGlvbnMpXG59XG5cbmZ1bmN0aW9uIG1hdGNoZXMgKHBhdHRlcm5zLCB2YWx1ZSkge1xuICByZXR1cm4gcGF0dGVybnMuc29tZShmdW5jdGlvbiAocGF0dGVybikge1xuICAgIHJldHVybiB0eXBlb2YgcGF0dGVybiA9PT0gJ3N0cmluZydcbiAgICAgID8gcGF0dGVybiA9PT0gdmFsdWVcbiAgICAgIDogcGF0dGVybi50ZXN0KHZhbHVlKVxuICB9KVxufVxuIl0sIm5hbWVzIjpbIm1hcCIsInJlcXVpcmUiLCJfcmVxdWlyZSIsInNuYWtlQ2FzZSIsIm1vZHVsZSIsImV4cG9ydHMiLCJvYmoiLCJvcHRpb25zIiwiT2JqZWN0IiwiYXNzaWduIiwiZGVlcCIsImV4Y2x1ZGUiLCJwYXJzaW5nT3B0aW9ucyIsImtleSIsInZhbCIsIm1hdGNoZXMiLCJwYXR0ZXJucyIsInZhbHVlIiwic29tZSIsInBhdHRlcm4iLCJ0ZXN0Il0sInNvdXJjZVJvb3QiOiIifQ==\n//# sourceURL=webpack-internal:///(rsc)/./node_modules/snakecase-keys/index.js\n");

/***/ })

};
;