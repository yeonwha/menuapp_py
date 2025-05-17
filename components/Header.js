/**
 * 
 * @returns Header for the title
 */
export default function Header() {
    return (
      <header className='border-b border-gray-200 mx-8 mb-4 pb-2'>
        <div className="container px-4 flex justify-between items-center">
          <div className="flex-1 text-sm font-bold text-center">
            <p className="header_text text-2xl">
              Displaying Menu App
            </p>
          </div>
        </div>
      </header>
    )
}