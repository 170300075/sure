import { useForm } from "react-hook-form";
import { Button, Checkbox, Label, Spinner, TextInput } from "flowbite-react";
import { Card } from "flowbite-react";

function LoginForm() {
  const { register, handleSubmit, formState: { errors } } = useForm();

  const onSubmit = (data) => {
    console.log(data);
  };

  return (
    <div className="max-w-2xl">
      <Card horizontal={true} imgSrc="assets/cover.jpeg">
        <h5 className="text-2xl font-bold tracking-tight text-gray-900 dark:text-white text-center"><span className="italic">SURE Platforms</span></h5>

        <form className="flex flex-col gap-4 p-4" onSubmit={handleSubmit(onSubmit)}>
          {/* Campo de matrícula */}
          <div>
            <Label htmlFor="id_user" value="Tu matrícula"/>
            <TextInput 
              id="id_user" 
              type="number" 
              required={true} 
              placeholder="Ingresa tu matrícula"
              {...register("id_user", {
                required: true,
                pattern: /^\d{9}$/
              })}
              className={`${
                errors.id_user ? 'border-2 border-red-500 bg-red-100 active:ring-0 active:ring-red-500' : 'active:ring-0 focus:ring-info border-info'
              } rounded-lg ${
                errors.id_user ? 'invalid' : ''
              }`}
            />
            {errors.id_user && <p className="text-red-500 text-sm">La matrícula debe tener exactamente 9 dígitos.</p>}
          </div>

          {/* Campo de contraseña */}
          <div>
            <Label htmlFor="password" value="Tu contraseña actual"/>
            <TextInput id="password" type="password" required={true} helperText="🛈 Necesitamos tus credenciales de SIGMAA para obtener tu información escolar actualizada." placeholder="Ingresa tu contraseña"/>
          </div>

          {/* Opción para mantener sesión */}
          <div className="flex items-center gap-2">
            <Checkbox id="remember"/>
            <Label htmlFor="remember">Mantener sesión</Label>
          </div>

          {/* Botón de entrar */}
          <Button type="login" className="bg-gradient-to-r from-green-400 to-blue-500 hover:from-pink-500 hover:to-yellow-500" color="dark"> 
            {/* Ícono y animación del Spinner */}
            <Spinner color="gray" size="sm" animation={"border"} />
            <span className="pl-3">Entrar</span>
          </Button>
        </form>
      </Card>
    </div>
  );
}

function App() {
  return (
    <div className="h-screen flex items-center justify-center bg-gray-50">
      <LoginForm/>
    </div>
  );
}

export default App;
