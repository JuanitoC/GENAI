{
 "cells": [
  {
   "cell_type": "markdown",
   "id": "c49114b5-259b-4d9d-8511-649dd4042a88",
   "metadata": {},
   "source": [
    "## Javascript and LLM Apps\n",
    "* Programming language of the web applications.\n",
    "* For frontend and backend."
   ]
  },
  {
   "cell_type": "markdown",
   "id": "622194c8-e9f7-4c62-9bed-8ad2bd81bc03",
   "metadata": {},
   "source": [
    "## Instead of print(), console.log()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 61,
   "id": "0bd2f151-6512-4a1a-b574-aa1f7fcc75b0",
   "metadata": {},
   "outputs": [
    {
     "data": {
      "application/javascript": [
       "window.alert('printed in the console of the browser');\n"
      ],
      "text/plain": [
       "<IPython.core.display.Javascript object>"
      ]
     },
     "metadata": {},
     "output_type": "display_data"
    }
   ],
   "source": [
    "%%javascript\n",
    "window.alert('printed in the console of the browser');"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "0e0d99fd-cfc2-41e3-bbf9-eb9a05a231b5",
   "metadata": {},
   "source": [
    "## Semicolon at the end of each statement"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "d0e01f98-8dbf-42c5-ad51-bdf7d4313552",
   "metadata": {},
   "source": [
    "## Declare variables... or not"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 12,
   "id": "2aee2f1f-1bef-4a7f-9ace-eecd0ac21b24",
   "metadata": {},
   "outputs": [
    {
     "data": {
      "application/javascript": [
       "var x = 5; //old way\n",
       "let y = \"hello\";\n",
       "//z = 10;\n"
      ],
      "text/plain": [
       "<IPython.core.display.Javascript object>"
      ]
     },
     "metadata": {},
     "output_type": "display_data"
    }
   ],
   "source": [
    "%%javascript\n",
    "var x = 5; //old way\n",
    "let y = \"hello\";\n",
    "z = 10;"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 18,
   "id": "8b665fa8-7210-4347-9e98-e3b9517d00d2",
   "metadata": {},
   "outputs": [
    {
     "data": {
      "application/javascript": [
       "let x = 5;\n",
       "//let x = 6; let cannot redeclare\n",
       "x = 6;\n",
       "window.alert(x);\n"
      ],
      "text/plain": [
       "<IPython.core.display.Javascript object>"
      ]
     },
     "metadata": {},
     "output_type": "display_data"
    }
   ],
   "source": [
    "%%javascript\n",
    "let x = 5;\n",
    "//let x = 6; let cannot redeclare\n",
    "x = 6;\n",
    "window.alert(x);"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "36869739-9474-4fe8-8b95-5c5d026e92dd",
   "metadata": {},
   "source": [
    "## Peculiar Data Types\n",
    "* Objects. "
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 21,
   "id": "e42fa745-dcf0-4884-ab41-4c615d5bd7f4",
   "metadata": {},
   "outputs": [
    {
     "data": {
      "application/javascript": [
       "const myObject = {\n",
       "    brand: \"Honda\",\n",
       "    model: \"Odissey\"\n",
       "};\n"
      ],
      "text/plain": [
       "<IPython.core.display.Javascript object>"
      ]
     },
     "metadata": {},
     "output_type": "display_data"
    }
   ],
   "source": [
    "%%javascript\n",
    "const myObject = {\n",
    "    brand: \"Honda\",\n",
    "    model: \"Odissey\"\n",
    "};"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "edbd7df4-218c-43b7-be44-9f2dd83d8b77",
   "metadata": {},
   "source": [
    "## Functions"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 27,
   "id": "2ceb1bec-96c9-4bef-a6e4-e3f260f8f88c",
   "metadata": {},
   "outputs": [
    {
     "data": {
      "application/javascript": [
       "function my_function(parameter) {\n",
       "    return(\"Hello\" + parameter);    \n",
       "}\n"
      ],
      "text/plain": [
       "<IPython.core.display.Javascript object>"
      ]
     },
     "metadata": {},
     "output_type": "display_data"
    }
   ],
   "source": [
    "%%javascript\n",
    "function my_function(parameter) {\n",
    "    return(\"Hello\" + parameter);    \n",
    "}"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 28,
   "id": "371768a2-f4c6-4ef5-8e39-65c610d3c03e",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Hello! argument\n"
     ]
    }
   ],
   "source": [
    "my_function(\"argument\")"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "25b5515b-4b24-4096-9882-aa8bb316072b",
   "metadata": {},
   "source": [
    "#### Peculiar things to know about JS functions:\n",
    "* Arrow Functions"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 30,
   "id": "31c5d9b2-5400-42ad-a56d-15d3f50c298f",
   "metadata": {},
   "outputs": [
    {
     "data": {
      "application/javascript": [
       "let my_arrow_function = (parameter) => \"Hello\" + parameter;\n"
      ],
      "text/plain": [
       "<IPython.core.display.Javascript object>"
      ]
     },
     "metadata": {},
     "output_type": "display_data"
    }
   ],
   "source": [
    "%%javascript\n",
    "let my_arrow_function = (parameter) => \"Hello\" + parameter;"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 31,
   "id": "c1e6d79a-877e-4002-a8bc-c624bf96779d",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Hello! argument\n"
     ]
    }
   ],
   "source": [
    "my_function(\"argument\")"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "5c5a4712-a763-42a4-a2a1-18554cf296f2",
   "metadata": {},
   "source": [
    "* Use of Arrow Function as an anonymous function inside another Arrow function."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 40,
   "id": "2836f968-f9cf-4746-9b5a-b26c41e74fab",
   "metadata": {},
   "outputs": [
    {
     "data": {
      "application/javascript": [
       "const matchMaker = person1 => person2 => `${person2} marries ${person1}`;\n",
       "let newCouple = matchMaker(\"Robert Mitchum\");\n",
       "window.alert(newCouple(\"Ava Gardner\"));\n"
      ],
      "text/plain": [
       "<IPython.core.display.Javascript object>"
      ]
     },
     "metadata": {},
     "output_type": "display_data"
    }
   ],
   "source": [
    "%%javascript\n",
    "const matchMaker = person1 => person2 => `${person2} marries ${person1}`;\n",
    "let newCouple = matchMaker(\"Robert Mitchum\");\n",
    "window.alert(newCouple(\"Ava Gardner\"));"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "ae63b3b1-7214-4cd2-b2d9-73df3d99e2bb",
   "metadata": {},
   "source": [
    "## Classes\n",
    "* A class is like a blueprint to create objects."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 62,
   "id": "ba5c437a-3558-44e7-9096-a625efce92b8",
   "metadata": {},
   "outputs": [
    {
     "data": {
      "application/javascript": [
       "class Dog {\n",
       "    constructor(species) {\n",
       "        this.species = \"dog\";\n",
       "    }\n",
       "}\n",
       "const fido = new Dog()\n",
       "window.alert(fido.species)\n"
      ],
      "text/plain": [
       "<IPython.core.display.Javascript object>"
      ]
     },
     "metadata": {},
     "output_type": "display_data"
    }
   ],
   "source": [
    "%%javascript\n",
    "class Dog {\n",
    "    constructor(species) {\n",
    "        this.species = \"dog\";\n",
    "    }\n",
    "}\n",
    "const fido = new Dog()\n",
    "window.alert(fido.species)"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "d9f5feed-717d-410a-b76d-dc61ede211cc",
   "metadata": {},
   "source": [
    "## Object Methods"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 63,
   "id": "a446c8b4-04f6-4fa9-8f83-dcbac53d405b",
   "metadata": {},
   "outputs": [
    {
     "data": {
      "application/javascript": [
       "class Horse {\n",
       "    constructor(species, name, age, color) {\n",
       "        this.species = species;\n",
       "        this.name = name;\n",
       "        this.age = age;\n",
       "        this.color = color;\n",
       "    }\n",
       "    greetings() {\n",
       "        return \"Hello, my name is \" + this.name;\n",
       "    }\n",
       "}\n",
       "const jumper = new Horse(\"horse\", \"Jumper\", 3, \"brown\");\n",
       "window.alert(jumper.greetings());\n"
      ],
      "text/plain": [
       "<IPython.core.display.Javascript object>"
      ]
     },
     "metadata": {},
     "output_type": "display_data"
    }
   ],
   "source": [
    "%%javascript\n",
    "class Horse {\n",
    "    constructor(species, name, age, color) {\n",
    "        this.species = species;\n",
    "        this.name = name;\n",
    "        this.age = age;\n",
    "        this.color = color;\n",
    "    }\n",
    "    greetings() {\n",
    "        return \"Hello, my name is \" + this.name;\n",
    "    }\n",
    "}\n",
    "const jumper = new Horse(\"horse\", \"Jumper\", 3, \"brown\");\n",
    "window.alert(jumper.greetings());"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "9ee10c64-6c5c-4d78-869f-881096ad34a9",
   "metadata": {},
   "source": [
    "## Object Properties"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 50,
   "id": "2c638555-ca6b-496c-bc9a-a3b6312b7ff4",
   "metadata": {},
   "outputs": [
    {
     "data": {
      "application/javascript": [
       "class Horse {\n",
       "    constructor(species, name, age, color) {\n",
       "        this.species = species;\n",
       "        this.name = name;\n",
       "        this.age = age;\n",
       "        this.color = color;\n",
       "    }\n",
       "    greetings() {\n",
       "        return \"Hello, my name is \" + this.name;\n",
       "    }\n",
       "}\n",
       "const seabiscuit = new Horse(\"horse\", \"Seabiscuit\", 2, \"black\");\n",
       "seabiscuit.color = \"brown\";\n",
       "window.alert(seabiscuit.color);\n"
      ],
      "text/plain": [
       "<IPython.core.display.Javascript object>"
      ]
     },
     "metadata": {},
     "output_type": "display_data"
    }
   ],
   "source": [
    "%%javascript\n",
    "class Horse {\n",
    "    constructor(species, name, age, color) {\n",
    "        this.species = species;\n",
    "        this.name = name;\n",
    "        this.age = age;\n",
    "        this.color = color;\n",
    "    }\n",
    "    greetings() {\n",
    "        return \"Hello, my name is \" + this.name;\n",
    "    }\n",
    "}\n",
    "const seabiscuit = new Horse(\"horse\", \"Seabiscuit\", 2, \"black\");\n",
    "seabiscuit.color = \"brown\";\n",
    "window.alert(seabiscuit.color);"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "fbf66228-c2f3-4644-ab76-30b2c2b97e7e",
   "metadata": {},
   "source": [
    "## Inheritance"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 56,
   "id": "9c909989-f908-415d-ba71-96d9a075772e",
   "metadata": {},
   "outputs": [
    {
     "data": {
      "application/javascript": [
       "class Person {\n",
       "  constructor(fname, lname) {\n",
       "    this.firstname = fname;\n",
       "    this.lastname = lname;\n",
       "  }\n",
       "\n",
       "  printname() {\n",
       "    return(this.firstname + \" \" + this.lastname);\n",
       "  }\n",
       "}\n",
       "\n",
       "class Student extends Person {\n",
       "\n",
       "}\n",
       "\n",
       "const x = new Student(\"Mike\", \"Olsen\");\n",
       "window.alert(x.printname());\n"
      ],
      "text/plain": [
       "<IPython.core.display.Javascript object>"
      ]
     },
     "metadata": {},
     "output_type": "display_data"
    }
   ],
   "source": [
    "%%javascript\n",
    "class Person {\n",
    "  constructor(fname, lname) {\n",
    "    this.firstname = fname;\n",
    "    this.lastname = lname;\n",
    "  }\n",
    "\n",
    "  printname() {\n",
    "    return(this.firstname + \" \" + this.lastname);\n",
    "  }\n",
    "}\n",
    "\n",
    "class Student extends Person {\n",
    "\n",
    "}\n",
    "\n",
    "const x = new Student(\"Mike\", \"Olsen\");\n",
    "window.alert(x.printname());\n"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "a99670eb-1761-4859-b479-98e2df44da36",
   "metadata": {},
   "source": [
    "## Debugging"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 57,
   "id": "2d628e0f-d6c4-42a7-9745-4873387156b5",
   "metadata": {},
   "outputs": [
    {
     "data": {
      "application/javascript": [
       "try {\n",
       "  window.alert(\"all good!\");\n",
       "} catch (error) {\n",
       "  window.alert(\"An exception occurred\");\n",
       "}\n"
      ],
      "text/plain": [
       "<IPython.core.display.Javascript object>"
      ]
     },
     "metadata": {},
     "output_type": "display_data"
    }
   ],
   "source": [
    "%%javascript\n",
    "try {\n",
    "  window.alert(\"all good!\");\n",
    "} catch (error) {\n",
    "  window.alert(\"An exception occurred\");\n",
    "}\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 59,
   "id": "f2dde2f1-ca16-4150-8360-a9113f4979f2",
   "metadata": {},
   "outputs": [
    {
     "data": {
      "application/javascript": [
       "let x = -1;\n",
       "\n",
       "if (x < 0) {\n",
       "  throw new Error(\"Sorry, no numbers below zero\");\n",
       "}\n"
      ],
      "text/plain": [
       "<IPython.core.display.Javascript object>"
      ]
     },
     "metadata": {},
     "output_type": "display_data"
    }
   ],
   "source": [
    "%%javascript\n",
    "let x = -1;\n",
    "\n",
    "if (x < 0) {\n",
    "  throw new Error(\"Sorry, no numbers below zero\");\n",
    "}\n"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "f036d1e8-689b-4324-ac8c-958f785d3127",
   "metadata": {},
   "source": [
    "## How to get user input"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 64,
   "id": "ac6eaec4-0f03-4227-b9df-1a7ce23955e5",
   "metadata": {},
   "outputs": [
    {
     "data": {
      "application/javascript": [
       "let username = prompt(\"enter username: \");\n",
       "window.alert(\"your username is: \" + username);\n"
      ],
      "text/plain": [
       "<IPython.core.display.Javascript object>"
      ]
     },
     "metadata": {},
     "output_type": "display_data"
    }
   ],
   "source": [
    "%%javascript\n",
    "let username = prompt(\"enter username: \");\n",
    "window.alert(\"your username is: \" + username);"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "3f05ba83-412e-4976-9cfa-427176d7920c",
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3 (ipykernel)",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.11.4"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}