import { Resend } from "resend";

const resend = new Resend(
  process.env.RESEND_API_KEY
);

export async function POST(
  request: Request
) {
  try {
    const {
      name,
      email,
      message,
    } = await request.json();

    const data = await resend.emails.send({
      from: "Portfolio Contact <onboarding@resend.dev>",
      to: ["sharipovaritacontact@gmail.com"],
      subject: `New Portfolio Message from ${name}`,
      html: `
        <h2>New Contact Form Submission</h2>

        <p><strong>Name:</strong> ${name}</p>

        <p><strong>Email:</strong> ${email}</p>

        <p><strong>Message:</strong></p>

        <p>${message}</p>
      `,
    });

    return Response.json(data);

  } catch (error) {

    return Response.json(
      { error },
      { status: 500 }
    );
  }
}