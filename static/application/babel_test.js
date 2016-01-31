class Person {
	constructor(name, age){
		this.name = name;
		this.age = age;
	}

	sayHello(){
		log(this.name + ', Hello !')
	}
}

let person = new Person('Oregu', 19)
person.sayHello()