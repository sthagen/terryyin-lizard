import unittest
from lizard import analyze_file, FileAnalyzer, get_extensions
from lizard_languages import VueReader


def get_vue_function_list(source_code):
    return analyze_file.analyze_source_code("a.vue", source_code).function_list


class TestVue(unittest.TestCase):

    def test_empty(self):
        functions = get_vue_function_list("")
        self.assertEqual(0, len(functions))

    def test_simple_js_function(self):
        code = '''
        <template>
            <div>Hello</div>
        </template>
        <script>
            export default {
                methods: {
                    hello() {
                        return "world"
                    }
                }
            }
        </script>
        '''
        functions = get_vue_function_list(code)
        self.assertEqual(["hello"], [f.name for f in functions])

    def test_ts_function(self):
        code = '''
        <template>
            <div>Hello</div>
        </template>
        <script lang="ts">
            export default {
                methods: {
                    hello(): string {
                        return "world"
                    }
                }
            }
        </script>
        '''
        functions = get_vue_function_list(code)
        self.assertEqual(1, len(functions))
        self.assertEqual("hello", functions[0].name)

    def test_multiple_functions(self):
        code = '''
        <script>
            function helper1() {
                return 1;
            }
            export default {
                methods: {
                    method1() {
                        return helper1();
                    },
                    method2() {
                        if (true) {
                            return 2;
                        }
                        return 3;
                    }
                }
            }
        </script>
        '''
        functions = get_vue_function_list(code)
        self.assertEqual(["helper1", "method1", "method2"], [f.name for f in functions])
        self.assertEqual(2, functions[2].cyclomatic_complexity)