import unittest
from rcd.rcd_tree import Tree
from rcd.rcd_tree import build_tree
from rcd.rcd_tree import is_deadlock


class RcdTreeTest(unittest.TestCase):
    def setUp(self):
        self.tree1 = Tree("if", 1, None, None)
        self.function_body = """void* run_job(void *args)
{	
	std::string job_definition {static_cast<const char*>(args)};
	//std::cout<<job_definition <<std::endl;
	Job user_job {convert_job_string_to_vector(job_definition)};
	const auto tmp_date_obj {std::chrono::system_clock::to_time_t(std::chrono::system_clock::now())};
	std::vector<std::string> actual_date {convert_job_string_to_vector(std::ctime(&tmp_date_obj))};
	
	int err_no {pthread_mutex_lock(&m)};
	if (err_no)
	{
		std::cerr<< "Error nr. " <<err_no << " " << strerror(err_no) <<std::endl;
		return nullptr;
	}
	if (user_job.is_day_of_week(actual_date.at(0)) && user_job.is_month(actual_date.at(1)) && user_job.is_month_day(actual_date.at(2)) && user_job.is_time(actual_date.at(3)))
	{
		if (user_job.month_day != "29" && user_job.month != "2" && user_job.minutes != "59" && user_job.hours != "23" && user_job.day_of_week != "Sut")
		{
			user_job.call_job();
			pthread_mutex_unlock(&m);
		}
		else
		{
			user_job.call_job();
			std::cout<<"What a funny day!";
		}
	}
	else
	{
		pthread_mutex_unlock(&m);
	}
	//std::cout<<std::ctime(&tmp_date_obj) <<std::endl;
	//std::cout<< user_job <<std::endl;
	return nullptr;
}
        """

    def tearDown(self):
        del self.tree1

    def test_name(self):
        self.assertEqual(self.tree1.body, "if")
        self.assertTrue(repr(self.tree1).startswith("Tree<"))
        self.assertTrue(repr(self.tree1).endswith(">"))

    def test_build(self):
        braces_num = 0
        tokens = list()
        for line in self.function_body.split('\n'):
            line = line.strip()
            if line.startswith("if") or line.startswith("else"):
                tokens.append((line, braces_num, "run"))
            braces_num += line.count("{") - line.count("}")
            if "pthread_mutex_lock" in line:
                tokens.append((line, braces_num, "run"))
            if "pthread_mutex_unlock" in line:
                tokens.append((line, braces_num, "run"))

        trees = build_tree(tokens)
        self.assertEqual(len(trees), 4)

        self.assertIsNotNone(trees[0])
        self.assertIsNone(trees[0].left)
        self.assertIsNone(trees[0].right)

        self.assertIsNotNone(trees[1])
        self.assertIsNone(trees[1].left)
        self.assertIsNone(trees[1].right)

        self.assertIsNotNone(trees[2])
        self.assertIsNotNone(trees[2].left)
        self.assertIsNotNone(trees[2].right)
        self.assertIsNone(trees[2].left.left)
        self.assertIsNone(trees[2].left.right)
        self.assertIsNone(trees[2].right.right)
        self.assertIsNone(trees[2].right.left)

        self.assertIsNotNone(trees[3])
        self.assertIsNone(trees[3].left)
        self.assertIsNone(trees[3].right)


if __name__ == '__main__':
    unittest.main()
